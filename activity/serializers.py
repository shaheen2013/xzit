from rest_framework import serializers, status
from rest_framework.response import Response
from activity.models import Post, PostComment, PostImage, PostLike, PostSave, PostShare, Story
from django_q.tasks import async_task
from authentication.serializers import UserProfileSerializer

from common.models import Report

class PostImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image_path']


class PostCommentSerializer(serializers.ModelSerializer):
    extra_kwargs={
        'id': {'read_only': True},
        'created_by': {'read_only': True},
    }

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'created_by', 'comment']  


class PostCommentShowSerializer(serializers.ModelSerializer):
    created_by = UserProfileSerializer()

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'created_by', 'comment']  


class PostLikeSerializer(serializers.ModelSerializer):
    created_by = UserProfileSerializer()
    class Meta:
        model = PostLike
        fields = ('id', 'created_by')


class PostSaveSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = PostSave
        fields = ('post',)
        
    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data.get('post')
        userPostSave = PostSave.objects.filter(created_by=user, post_id=post.id).first()
        if userPostSave is not None:
            userPostSave.delete()
            return userPostSave
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance



class PostSaveSerializerGet(serializers.ModelSerializer):
    created_by = UserProfileSerializer()
    class Meta:
        model = PostSave
        fields = ('id','created_by',)




class PostSerializerGet(serializers.ModelSerializer):
    created_by = UserProfileSerializer()
    postimages = PostImageUrlSerializer(many=True, read_only=True, source='postimage')
    postcomments = PostCommentShowSerializer(many=True, read_only=True, source='postcomment')
    post_liker = PostLikeSerializer(many=True, source='postlike')
    extra_kwargs = {
        'id': {'read_only' : True},
        'created_at': {'read_only': True},
    }
    post_likes = serializers.SerializerMethodField(method_name='count_likes')
    post_save = PostSaveSerializerGet(many=True, source='postSave')

    def count_likes(self, instance: Post):
        count = instance.postlike.all().count()
        return count

    class Meta:
        model = Post
        fields = ('id', 'description', 'location', 'created_by', 'postimages', 'postcomments','post_likes','post_liker','post_save')
    

class PostSerializerPostPutPatch(serializers.ModelSerializer):
    extra_kwargs = {
        'id': {'read_only' : True},
        'created_at': {'read_only': True},
    }
    class Meta:
        model = Post
        fields = ('id','description', 'location')
    




class PostShareSerializerGet(serializers.ModelSerializer):
    post = PostSerializerGet()
    share_by = serializers.IntegerField(source='created_by_id')
    class Meta:
        model = PostShare
        fields = ('id', 'post', 'comment', 'share_by',)

class PostShareSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = PostShare
        fields = ('post','comment')
        
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     post = validated_data.get('post')
    #     userPostSave = PostSave.objects.filter(created_by=user, post_id=post.id).first()
    #     if userPostSave is not None:
    #         userPostSave.delete()
    #         return userPostSave
    #     instance = self.Meta.model(**validated_data)
    #     instance.save()
    #     return instance





class PostManageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ['total_shares', 'container_ratio']
        


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
        async_task("common.services.sleep_and_remove", obj=instance, hook="common.services.hook_after_sleep")
        return instance
    

class StorySerializerDetails(serializers.ModelSerializer):
    created_by = UserProfileSerializer()
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
        async_task("common.services.sleep_and_remove", obj=instance, hook="common.services.hook_after_sleep")
        return instance

        
    
class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('reason', 'description', 'post')
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.report_type = "Post"
        instance.save()
        return instance
    
class StoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('reason', 'description', 'story')
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.report_type = "Story"
        instance.save()
        return instance


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('post', 'image_path')

    extra_kwargs = {
        'image_path': {'required': True}
    }

        
        
        