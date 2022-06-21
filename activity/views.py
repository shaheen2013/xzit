from django.shortcuts import render
from rest_framework import generics
from activity.models import Post, PostLike, Story
from activity.serializers import PostInterectionSerializer, PostSerializer, StorySerializer
from rest_framework.permissions import IsAuthenticated

from xzit.mixins.models import CustomPagination


# Create your views here.

class PostListApiView(generics.ListCreateAPIView):
       serializer_class=PostSerializer
       queryset=Post.objects.all()
       # authentication_classes = [SessionAuthentication, BasicAuthentication]
       permission_classes = [IsAuthenticated]
       pagination_class = CustomPagination
       
       def get_queryset(self):
              return Post.objects.filter(created_by=self.request.user)
       
       
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
       

class StoryCreateListAPIView(generics.ListCreateAPIView):
       serializer_class=StorySerializer
       queryset = Story.objects.all()
       permission_classes = [IsAuthenticated] 
       
class StoryRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
       serializer_class = StorySerializer
       queryset = Story.objects.all()
       lookup_field = 'id'
       permission_classes = [IsAuthenticated]