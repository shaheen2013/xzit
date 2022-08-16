from rest_framework.response import Response
from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.models import Group
from commerce.models import BusinessType
from common.models import Report
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Permission, Group
from xzit.emails import send_otp, send_reset_otp
from django.shortcuts import get_object_or_404


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
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'phone', 'password', 'tokens', 'otp', 'profile_image')
        extra_kwargs = {
            'password': {'write_only': True},
            'otp': {'read_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
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
    class Meta:
        model = User
        fields = ('id','business_name', 'business_manager', 'business_type',
                  'business_address', 'country', 'city', 'bio', 'amenties', 'location')


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField()
    new_password = serializers.CharField()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class LoginSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email', 'role', 'tokens')


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


class BusinessSubTypeSaveSerializer(serializers.ModelSerializer):
    extra_kwargs = {
            'id': {'read_only': True}
        }
    class Meta:
        model = User
        fields = ('id', 'business_sub_type')


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


class BusinessTypeSaveSerializer(serializers.ModelSerializer):
    business_type = BusinessTypesSerializer(many=True)
    extra_kwargs = {
        'id': {'read_only': True}
    }
    class Meta:
        model = User
        fields = ('id', 'business_type') 
class UserProfileSerializer(serializers.ModelSerializer):
    extra_kwargs = {
            'id': {'read_only': True},
            'role': {'read_only': True},
        }
    business_type = BusinessTypesSerializer(many=True)
    business_sub_type = BusinessTypesSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'email', 'birth_date', 'bio', 'location', 'phone', 'business_type', 'business_sub_type', 'profile_image', 'cover_image')

class MerchantProfileSerializer(serializers.ModelSerializer):
    business_type = BusinessTypesSerializer(many=True)
    extra_kwargs = {
            'id': {'read_only': True},
            'role': {'read_only': True},
        }
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'birth_date', 'bio', 'location', 'phone', 'business_type', 'business_sub_type', 'profile_image', 'cover_image', 'business_manager', 'business_phone', 'business_address', 'business_hours', 'amenties')
        
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
    


class BusinessInterestSubSerializer(serializers.Serializer):
    business_type = serializers.PrimaryKeyRelatedField(queryset=BusinessType.objects.all(), many=False)
    business_sub_type = serializers.PrimaryKeyRelatedField(
        queryset=BusinessType.objects.all(), many=True
    )

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


class BusinessInterestSerializer(serializers.Serializer):
    type = serializers.ListField(child=BusinessInterestSubSerializer())