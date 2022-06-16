from rest_framework import serializers

from authentication.models import User
from xzit.settings import AUTH_USER_MODEL


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'phone', 'password')
