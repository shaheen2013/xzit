from django.shortcuts import render
from rest_framework import generics
from activity.models import Post, PostLike
from activity.serializers import PostInterectionSerializer, PostSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from xzit.mixins.models import CustomPagination


# Create your views here.

class PostListApiView(generics.ListCreateAPIView):
       serializer_class=PostSerializer
       queryset=Post.objects.all()
       # authentication_classes = [SessionAuthentication, BasicAuthentication]
       permission_classes = [IsAuthenticated]
       pagination_class = CustomPagination
       
       
class PostUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
       serializer_class=PostSerializer
       queryset=Post.objects.all()
       lookup_field= 'id'
       permission_classes = [IsAuthenticated]
       
class PostInterectionCreateAPIView(generics.CreateAPIView):
       serializer_class=PostInterectionSerializer
       lookup_field = 'id'
       queryset = PostLike.objects.all()
       permission_classes = [IsAuthenticated]
       