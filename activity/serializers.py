from rest_framework import serializers
from activity.models import Post, PostLike, Story
from authentication.serializers import RegistrationSerializer

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
        