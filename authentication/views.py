from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from authentication import serializers

class UserRegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    
class UserBasicInfoUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.UserBasicInfoUpdateSerializer
    
class MerchantRegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.MerchantRegisterSerializer
    
class MerchantBasicInfoUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.MerchantBasicInfoUpdateSerializer
