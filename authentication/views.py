from urllib import response
from rest_framework import generics, status
from rest_framework.views import APIView
from authentication import serializers
from authentication.models import User, XzitPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from commerce.models import BusinessType
from common.models import Report
from xzit.emails import send_otp
from django.contrib.auth.models import Permission, Group
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from xzit.mixins.models import CustomPagination


class UserRegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)


class AdminRegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.AdminRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)



    
class UserBasicInfoUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.UserBasicInfoUpdateSerializer
    lookup_field = "id"
    queryset = User
    
class MerchantRegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.MerchantRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)
    
class MerchantBasicInfoUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.MerchantBasicInfoUpdateSerializer
    lookup_field = "id"
    queryset = User
    
class UserProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserProfileSerializer
    # parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.select_related('business_type').prefetch_related('business_sub_type').all()
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

class MerchantProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.MerchantProfileSerializer
    # parser_classes = (MultiPartParser, FormParser)
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
    
class AdminLogin(Login):
    serializer_class = serializers.AdminLoginSerializer
    def post(self, request, *args, **kwargs):
        """ Login system: User and Merchent both. """
        User = get_user_model()
        username = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if (username is None) or (password is None):
            raise exceptions.AuthenticationFailed('eamil and password required')

        user = User.objects.filter(email=username).first()
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

class PasswordResetConfirmAPIView(generics.CreateAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def create(self, request, *args, **kwargs):
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
        
class UsernameCheckAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.UsernameCheckSerialiezer
    queryset = User.objects.all()
    lookup_field = "username"
    
    def retrieve(self, request, *args, **kwargs):
        # if self.queryset().filter(username=request.username).exists():
        #     return Response({"message": "Username already taken."}, 409)
        
        # return Response({"message": "Username is available."}, 200)
        return super().retrieve(request, *args, **kwargs)



class PhoneNumberCheck(generics.CreateAPIView):
    serializer_class = serializers.UserPhoneCheck
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(phone=serializer.data.get('phone_number')).first()
        headers = self.get_success_headers(serializer.data)
        if user is None:
            return Response({
            'detail':'Congrasulation! phone number is avilable'
            }, status=status.HTTP_200_OK, headers=headers)
        return Response({
            'detail':'Phone number already used with another account.Try another phone number.'
        }, status=status.HTTP_409_CONFLICT, headers=headers)


class BusinessInterest(generics.CreateAPIView):
    queryset = User
    serializer_class = serializers.BusinessInterestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        b_type_dict = dict({
            'business_type':[],
            'business_sub_type':[],
        })
        
        for data in serializer.data.get('type'):
            for key, value in data.items():
                if type(value) is list:
                    b_type_dict[key].extend(value)
                else:
                    b_type_dict[key].append(value) 

        user = get_object_or_404(User, id=request.user.id)
        business_types = list(set(b_type_dict['business_type']))
        user.business_sub_type.clear()
        user.business_type.clear()
        for business_type in business_types:
            b_type = get_object_or_404(BusinessType, id=business_type)
            user.business_type.add(b_type)

        business_sub_types = list(set(b_type_dict['business_sub_type']))
        for business_sub_type in business_sub_types:
            b_type = get_object_or_404(BusinessType, id=business_sub_type)
            user.business_sub_type.add(b_type)

        serializer_user = serializers.UserProfileSerializer(user)
        return Response(serializer_user.data)
from rest_framework.views import APIView
class RoleAssignAPIView(generics.CreateAPIView):
    serializer_class = serializers.RoleAssignSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)   
        return Response({'success': 'Role has been assigned !'}, 200)



# user_permission branch 
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination



# from django.contrib.contenttypes.models import ContentType
from json import dumps
from rest_framework.parsers import JSONParser
class XzitPermissionAPIView(generics.ListAPIView):
    queryset = XzitPermission.objects.all()
    serializer_class = serializers.ContentTypeSerializer

    def list(self, request, *args, **kwargs):
        queryset = Permission.objects.select_related('content_type').values('id', 'name', 'content_type__model')

        objects = {}

        removal_permission = []

        for permission in queryset:
            if permission['content_type__model'] in removal_permission:
                continue
            objects[permission['content_type__model']]= []

        for permission in queryset:
            if permission['content_type__model'] in removal_permission:
                continue
            objects[permission['content_type__model']].append(permission)
        
        return Response({'permissions':objects})


