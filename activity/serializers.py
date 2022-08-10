from genericpath import exists
from rest_framework import serializers, status
from rest_framework.response import Response
from activity.models import Post, PostComment, PostImage, PostLike, Story
from django_q.tasks import async_task

from common.models import Report

class PostSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        'id': {'read_only' : True},
        'created_at': {'read_only': True}
    }
    class Meta:
        model = Post
        fields = ('id', 'description')
        
class PostManageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ['total_shares', 'container_ratio']
        

class PostCommentSerializer(serializers.ModelSerializer):
    extra_kwargs={
        'id': {'read_only': True},
        'created_by': {'read_only': True},
    }

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'created_by', 'comment']  

class PostInterectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('created_by', 'post')
        
    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data.get('post')
        userPostLike = PostLike.objects.filter(created_by=user, post_id=post.id).first()
        if userPostLike is not None:
            userPostLike.delete()
            return userPostLike
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    

class StorySerializer(serializers.ModelSerializer):
    
    extra_kwargs = {
        'story_time': {'read_only' : True},
        'created_by' : {'read_only': True}
    }

    class Meta:
        model=Story
        fields=('id', 'story_type', 'media', 'story_time', 'created_by')
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        async_task("activity.services.sleep_and_remove", obj=instance, hook="activity.services.hook_after_sleep")
        
        return instance
    
class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('reason', 'post')
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.report_type = "Post"
        instance.save()
        return instance
    
class StoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('reason', 'story')
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.report_type = "Story"
        instance.save()
        return instance


class PostImageSerializer(serializers.ModelSerializer):
    image_path = serializers.ImageField(required=True)
    class Meta:
        model = PostImage
        fields = ('post', 'image_path')

        
        
        