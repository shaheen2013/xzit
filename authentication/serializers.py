from httplib2 import Response
from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.models import Group

from xzit.emails import send_otp

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'password', 'tokens', 'otp')
        extra_kwargs = {
                'password' : { 'write_only' : True},
                'otp':  { 'read_only' : True}
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
    class Meta:
        model = User
        fields = ('age', 'gender', 'country', 'city')


class MerchantRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'password', 'tokens', 'otp')
        extra_kwargs = {
                'password' : { 'write_only' : True},
                'otp' : { 'read_only' : True}
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
     class Meta:
        model = User
        fields = ('business_name', 'business_manager', 'business_type', 'business_address', 'country','city', 'bio', 'amenties')
        
        
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
    