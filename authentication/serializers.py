from tokenize import group
from rest_framework.response import Response
from rest_framework import serializers
from authentication.models import Amenities, BusinessHour, User
from commerce.models import BusinessType
from common.models import Report
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Permission, Group
from xzit.emails import send_otp, send_reset_otp
from django.contrib.auth import password_validation as password_validator
from django.core import exceptions



class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = "__all__"


class BusinessHourSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    day = serializers.CharField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'phone', 'password', 'tokens', 'otp', 'profile_image')
        extra_kwargs = {
            'password': {'write_only': True},
            'otp':  {'read_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            try:
                password_validator.validate_password(password) 
                instance.set_password(password)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({
                    'password':e.messages
                })

                 
        instance.save()
        # OTP Send
        if instance.email is not None:
            send_otp(instance.email, instance)
        # Add Group
        user_group, created = Group.objects.get_or_create(name='user')
        user_group.user_set.add(instance)
        return instance



class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'phone', 'password', 'tokens', 'otp', 'profile_image')
        extra_kwargs = {
            'password': {'write_only': True},
            'otp':  {'read_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            try:
                password_validator.validate_password(password) 
                instance.set_password(password)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({
                    'password':e.messages
                })
        instance.is_superuser = True
        instance.is_staff = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        # OTP Send
        if instance.email is not None:
            send_otp(instance.email, instance)
        # Add Group
        user_group, created = Group.objects.get_or_create(name='user')
        user_group.user_set.add(instance)
        return instance

class UserBasicInfoUpdateSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        'id': {'read_only': True}
    }
    class Meta:
        model = User
        fields = ('id','age', 'gender', 'country', 'city', 'location')


class MerchantRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',
                  'email', 'phone', 'password', 'tokens', 'otp')
        extra_kwargs = {
            'password': {'write_only': True},
            'otp': {'read_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            try:
                password_validator.validate_password(password) 
                instance.set_password(password)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({
                    'password':e.messages
                })
        instance.save()
        # OTP Send
        if instance.email is not None:
            send_otp(instance.email, instance)
        # Add group
        merchant_group, created = Group.objects.get_or_create(name='merchant')
        instance.groups.add(merchant_group.id)
        return instance




class MerchantBasicInfoUpdateSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        'id': {'read_only': True}
    }
    business_hours = BusinessHourSerializer(required=False, many=True)
    class Meta:
        model = User
        fields = ('id', 'business_name', 'business_hours', 'business_manager', 'business_address', 'country', 'city', 'bio', 'amenties', 'location')

class MerchantProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField()
    new_password = serializers.CharField()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'email':{'required':True}
        }


class LoginSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'business_name', 'email', 'role', 'tokens', 'profile_image')


class OtpResendSerialize(serializers.Serializer):
    user = serializers.IntegerField()


class OtpVerifySerializer(serializers.Serializer):
    user = serializers.IntegerField()
    otp = serializers.CharField()


class AccountVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', )

    def create(self, validated_data):
        email = validated_data['email']
        if self.Meta.model.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            send_otp(email, user)
            return user

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', )

    def create(self, validated_data):
        email = validated_data['email']
        if self.Meta.model.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            send_reset_otp(email, user)
            return user
        else:
            raise serializers.ValidationError({'details':'user not exist!'})
        
class PasswordResetVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('reset_pass_otp', )
        extra_kwargs = {'reset_pass_otp': {'required': True, 'allow_blank': False}}


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField()
    id = serializers.IntegerField()
    reset_pass_otp = serializers.CharField()


class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('reason', 'description', 'user')
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.report_type = "User"
        instance.save()
        return instance


class BusinessTypesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BusinessType
        fields = ('id', 'name', 'icon')

class UserProfileSerializer(serializers.ModelSerializer):
    extra_kwargs = {
            'id': {'read_only': True},
            'role': {'read_only': True},
        }
    business_type = BusinessTypesSerializer(many=True)
    business_sub_type = BusinessTypesSerializer(many=True)
    full_name = serializers.SerializerMethodField(method_name='get_full_name')
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name','full_name', 'gender', 'email', 'birth_date', 'bio', 'location', 'phone', 'business_name', 'business_type', 'business_sub_type', 'profile_image', 'cover_image', 'role','is_active' )
    def get_full_name(self, instance:User):
        return instance.name()

class MerchantProfileSerializer(serializers.ModelSerializer):
    extra_kwargs = {
            'id': {'read_only': True},
            'role': {'read_only': True},
        }

    business_hours = BusinessHourSerializer(required=True, many=True, source='authentication_businesshour_related')
    amenties = AmenitiesSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'gender', 'birth_date', 'bio', 'location', 'country', 'city', 'phone','business_name', 'business_type', 'business_sub_type', 'profile_image', 'cover_image', 'business_manager', 'business_phone', 'business_address','business_hours', 'amenties','is_active',)

    def get_full_name(self, instance:User):
        return instance.name()    



class MerchantProfileSerializerPost(serializers.ModelSerializer):
    extra_kwargs = {
            'id': {'read_only': True},
            'role': {'read_only': True},
        }

    business_hours = BusinessHourSerializer(required=True, many=True, source='authentication_businesshour_related')
    class Meta:
        model = User
        fields = ('id', 'gender', 'birth_date', 'bio', 'location', 'country', 'city', 'phone','business_name', 'business_type', 'business_sub_type', 'profile_image', 'cover_image', 'business_manager', 'business_phone', 'business_address','business_hours', 'amenties','is_active',)


    
class PermissionSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Permission 
        fields = '__all__'
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class RoleDetailsSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    class Meta:
        model = Group
        fields = '__all__'

class UsernameCheckSerialiezer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', ) 
        


class UserPhoneCheck(serializers.Serializer):
    phone_number = serializers.CharField(required = True)
    
from django.shortcuts import get_object_or_404
class RoleAssignSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    role = serializers.IntegerField()
    
    def create(self, validated_data):
        user = get_object_or_404(User, id=validated_data['user'])
        role = get_object_or_404(Group, id=validated_data['role'])
        if user is None:
            raise serializers.ValidationError({
                'details': 'User not found'
            })
            
        if role is None:
            raise serializers.ValidationError({
                'details': 'Role not found'
            })
        user.groups.clear()
        
        role.user_set.add(user)

        return validated_data  

class BusinessInterestSubSerializer(serializers.Serializer):
    business_type = serializers.PrimaryKeyRelatedField(queryset=BusinessType.objects.all(), many=False)
    business_sub_type = serializers.PrimaryKeyRelatedField(
        queryset=BusinessType.objects.all(), many=True
    )

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


class BusinessInterestSerializer(serializers.Serializer):
    type = serializers.ListField(child=BusinessInterestSubSerializer())


class ModelLabelPermissionSeralizer(serializers.ModelSerializer):
    class Meta: 
        model = Permission 
        fields = ['id', 'name']


from django.contrib.contenttypes.models import ContentType

class ContentTypeSerializer(serializers.ModelSerializer):
    permissions = ModelLabelPermissionSeralizer(many = True, source='content_type_set')
    class Meta:
        model = ContentType
        fields = ['id', 'model', 'permissions']

    