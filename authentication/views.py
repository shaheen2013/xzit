from rest_framework import generics, status
from yaml import serialize
from authentication import serializers
from authentication.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from common.models import Report

from xzit.emails import send_otp

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
    queryset = User.objects.all()
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