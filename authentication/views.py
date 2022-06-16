from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from authentication.serializers import RegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
