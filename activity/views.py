from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from yaml import serialize
from activity.models import Post, PostComment, PostLike, Story
from activity import serializers
from rest_framework.permissions import IsAuthenticated
from xzit.mixins.models import CustomPagination
from datetime import timedelta
from django.utils import timezone

""" 
Activity - Post
- Crate Post
- View Post
- Update Post
- Delete Post
"""
class PostListApiView(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user)


class PostUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user)


class PostInterectionCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.PostInterectionSerializer
    lookup_field = 'id'
    queryset = PostLike.objects.all()
    permission_classes = [IsAuthenticated]


class PostCommentAPIView(generics.CreateAPIView):
    """ 
    - Create post comment
    - Show post Comments
    """
    serializer_class = serializers.PostCommentSerializer
    queryset = PostComment
    permission_classes = [IsAuthenticated]
    
class PostCommentsAPIView(generics.ListAPIView):
       serializer_class = serializers.PostCommentSerializer
       lookup_field= 'post_id'
       queryset = PostComment

       def get_queryset(self):
           return PostComment.objects.filter(post_id=self.kwargs['post_id'])

""" 
       Activity - Story 
       - Create Story
       - View Story
       - Update Story
       - Delete Story
"""
class StoryListCreateAPIView(generics.ListCreateAPIView):
    """
    New Story Create
    """
    serializer_class = serializers.StorySerializer
    queryset = Story.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Story.objects.filter(created_by=self.request.user)


class StoryRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StorySerializer
    queryset = Story.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Story.objects.filter(created_by=self.request.user)
    
    
def removeStories(request):
    lastHour = timezone.now() - timedelta(hours=1)
    stories = Story.objects.filter(created_at__gte=lastHour).values()
    stories = list(stories)
    
    return JsonResponse(stories, safe=False)
