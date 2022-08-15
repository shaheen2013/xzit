from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from yaml import serialize
from activity.models import Post, PostComment, PostImage, PostLike, Story
from activity import serializers
from rest_framework.permissions import IsAuthenticated
from common.models import Report
from xzit.mixins.models import CustomPagination
from datetime import timedelta
from django.utils import timezone

from rest_framework.parsers import MultiPartParser, FormParser

""" 
Activity - Post
- Crate Post
- View Post
- Update Post
- Delete Post
- Report Post
"""
class PostCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.PostSerializerPostPutPatch
    queryset = Post.objects.all()
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user)

class PostFeedListApiView(generics.ListAPIView):
    serializer_class = serializers.PostSerializerGet
    queryset = Post.objects.select_related('created_by').prefetch_related('postimage', 'postcomment','postlike').all()
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    pagination_class = CustomPagination

    # def get_queryset(self):
    #     return Post.objects.filter(created_by=self.request.user)


class PostDeleteApiView(generics.DestroyAPIView):
    serializer_class = serializers.PostSerializerGet
    queryset = Post.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for image in instance.postimage.all():
            image.image_path.delete(False)
        return super().destroy(request, *args, **kwargs)

class PostUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.PostSerializerPostPutPatch
    queryset = Post.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user)

class PostDetailsApiView(generics.RetrieveAPIView):
    serializer_class = serializers.PostSerializerGet
    queryset = Post.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


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
       serializer_class = serializers.PostCommentShowSerializer
       lookup_field= 'post_id'
       queryset = PostComment
       permission_classes = [IsAuthenticated]

       def get_queryset(self):
           return PostComment.objects.filter(post_id=self.kwargs['post_id'])
       
class PostReportApiView(generics.CreateAPIView):
    """
        Report to post
    """
    serializer_class = serializers.PostReportSerializer
    queryset = Report
    permission_classes = [IsAuthenticated]

""" 
       Activity - Story 
       - Create Story
       - View Story
       - Update Story
       - Delete Story
"""
class StoryListCreateAPIView(generics.ListCreateAPIView):
    """
        Story Create & List
    """
    serializer_class = serializers.StorySerializerDetails
    queryset = Story.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Story.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.StorySerializer
        return super().get_serializer_class()
    
class StoryFeedAPIView(generics.ListAPIView):
    """
    Story Feed
    """
    serializer_class = serializers.StorySerializerDetails
    queryset = Story.objects.all()


class StoryRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StorySerializerDetails
    queryset = Story.objects.all()
    lookup_field = 'id'
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method == "GET":
            return self.queryset
        return Story.objects.filter(created_by=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST','PUT', 'PATCH']:
            return serializers.StorySerializer
        return super().get_serializer_class()
 
class StoryReportApiView(generics.CreateAPIView):
    """
        Report to Story
    """
    serializer_class = serializers.StoryReportSerializer
    queryset = Report
    permission_classes = [IsAuthenticated]


class MyPostAPIList(generics.ListAPIView):
    """
        My Posts list.
    """
    serializer_class = serializers.PostSerializerGet
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user.id)

class PostImageAPIView(generics.CreateAPIView):
    serializer_class = serializers.PostImageSerializer
    queryset = PostImage
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
def removeStories(request):
    lastHour = timezone.now() - timedelta(hours=1)
    stories = Story.objects.filter(created_at__gte=lastHour).values()
    stories = list(stories)
    
    return JsonResponse(stories, safe=False)




