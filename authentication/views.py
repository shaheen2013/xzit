from rest_framework import generics, status
from rest_framework.views import APIView
from authentication import serializers
from authentication.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from common.models import Report
from xzit.emails import send_otp
from django.contrib.auth.models import Permission, Group

class UserRegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    
class UserBasicInfoUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.UserBasicInfoUpdateSerializer
    lookup_field = "id"
    queryset = User
    
class MerchantRegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.MerchantRegisterSerializer
    
class MerchantBasicInfoUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.MerchantBasicInfoUpdateSerializer
    lookup_field = "id"
    queryset = User
    
class UserProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserProfileSerializer
    queryset = User.objects.select_related('business_type').prefetch_related('business_sub_type').all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

class MerchantProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.MerchantProfileSerializer
    queryset = User.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
    
class ChangePasswordApiView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OtpResendpApiView(generics.GenericAPIView):
    serializer_class = serializers.OtpResendSerialize
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_obj = User.objects.filter(id=serializer.data.get('user')).first()
            if user_obj is None:
                return Response({'details': 'User not found !'}, 404)

            send_otp(user_obj.email, user_obj)
            return Response({'details' : 'Your new otp has been send.'})
        return Response({'details' : 'Invalid data'}, 400)

class OtpVerifyApiView(generics.GenericAPIView):
    serializer_class = serializers.OtpVerifySerializer

    def post(self, request, *args, **kwargs):
        serialize = self.get_serializer(data=request.data)
        if serialize.is_valid():
            user = User.objects.filter(id=serialize.data.get('user')).first()
            if user is None:
                return Response({'details': 'User not found !'})
            if serialize.data.get('otp') != user.otp:
                return Response({'details' : 'OTP does not match. Please try valid OTP.'}, 400)
            if user.is_verified:
                return Response({'details' : 'You are already verified.'}, 200)
            user.is_verified = True 
            user.save()
            login_details = serializers.LoginSuccessSerializer(user).data 
            return Response({'message': 'Congratulations! Your OTP has been verified.', 'login_details' : login_details}, 200)
            
        return Response({'details': 'Invalid data'}, 400)
        
class Login(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        """ Login system: User and Merchent both. """
        User = get_user_model()
        username = request.data.get('username')
        password = request.data.get('password')
        response = Response()
        if (username is None) or (password is None):
            raise exceptions.AuthenticationFailed('username and password required')

        user = User.objects.filter(username=username).first()
        if(user is None):
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
        
        if user.is_verified is not True: 
            return Response({'details' : 'You are not OTP verified. Please verify your OTP'})
        
        response.data = serializers.LoginSuccessSerializer(user).data
        return response
    
class AccountVerifyApiView(generics.CreateAPIView):
    serializer_class = serializers.AccountVerificationSerializer 
    queryset = User.objects.all()
    
class BusinessTypeSaveApiView(generics.UpdateAPIView):
    serializer_class = serializers.BusinessTypeSaveSerializer
    queryset = User.objects.all()
    lookup_field = "id"
    
class BusinessSubTypeSaveApiView(generics.UpdateAPIView):
    serializer_class = serializers.BusinessSubTypeSaveSerializer
    queryset = User.objects.all()
    lookup_field = "id"



class UserReportApiView(generics.CreateAPIView):
    """
        Report to User
    """
    serializer_class = serializers.UserReportSerializer
    queryset = Report
    permission_classes = [IsAuthenticated]
    
class PermissionAPIView(generics.ListAPIView):
    """ 
    All permissions. 
    """
    serializer_class = serializers.PermissionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.all()
    
class RolesCreateListApiView(generics.ListCreateAPIView):
    serializer_class = serializers.RoleSerializer
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.RoleDetailsSerializer
        return super().get_serializer_class()
    
class RolesRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RoleSerializer
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    lookup_field = "id"
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.RoleDetailsSerializer
        return super().get_serializer_class()
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({'success':'Your data has been updated.'})
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Your data has been deleted.'})
    



class PasswordResetAPIView(generics.CreateAPIView):
    serializer_class = serializers.PasswordResetSerializer
    queryset = User 

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"details" : "Your OTP has been sent your email"})




class PasswordResetOtpVerfy(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetVerifySerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        """ Login system: User and Merchent both. """
        User = get_user_model()
        otp = request.data.get('reset_pass_otp')
        response = Response()
        if (otp is None):
            raise exceptions.AuthenticationFailed('otp required')
        user = User.objects.filter(reset_pass_otp=otp).first()
        if(user is None):
            raise exceptions.AuthenticationFailed('otp not valid')

        response.data = serializers.UserProfileSerializer(user).data
        return response

# class PasswordResetConfirmAPIView(generics.GenericAPIView):
#     serializer_class = serializers.PasswordResetConfirmSerializer
#     queryset = User.objects.all()
    
#     def post(self, request, *args, **kwargs):
#         """ Login system: User and Merchent both. """
#         User = get_user_model()
#         id = request.data.get('id')
#         serializer = serializers.PasswordResetConfirmSerializer(request.data)
#         response = Response()
        
#         if serializer.is_valid():
#             user = User.objects.filter(id=request.data.get('id')).first()
#             user.reset_pass_otp = None
#             response.data = serializers.UserProfileSerializer(user).data
#             return response
#         else:
#             response.data = serializer.errors
#             return response.data



class PasswordResetConfirmAPIView(generics.UpdateAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.data.get('id'))
            print(user.id)
            if user is None:
                return Response({"details": "User not found !"}, 404)
            if user.reset_pass_otp != serializer.data.get('reset_pass_otp'):
                return Response({"details" : "Your OTP is wrong !"}, 400)

        user.set_password(serializer.data.get("password"))
        user.reset_pass_otp = None
        user.save()
        print(user)
        return Response( {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully'
        })