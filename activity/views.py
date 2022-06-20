from django.shortcuts import render
from rest_framework import generics
from activity.models import Post
from activity.serializers import PostSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PostApiView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
       serializer_class=PostSerializer
       queryset=Post.objects.all()
       # authentication_classes = [SessionAuthentication, BasicAuthentication]
       permission_classes = [IsAuthenticated]