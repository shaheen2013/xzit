from django.shortcuts import render
from requests import request

# Create your views here.
from rest_framework import generics
from authentication import serializers
from authentication.models import User

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
    
    
