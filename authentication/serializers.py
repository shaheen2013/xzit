from rest_framework import serializers

from authentication.models import User
from xzit.settings import AUTH_USER_MODEL

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'phone', 'password', 'tokens', 'business_days', 'business_hours', 'business_type', 'business_sub_type', 'device_type')
        extra_kwargs = {
            'password' : { 'write_only' : True}
        }
      
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        
        return instance
