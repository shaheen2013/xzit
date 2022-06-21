
from dataclasses import fields
from pyexpat import model
from wsgiref import validate
from rest_framework import serializers
from activity.models import Post, PostLike

class PostSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        'id': {'read_only' : True}
    }
    class Meta:
        model = Post
        fields = ('id', 'description', 'created_by', 'total_shares', 'container_ratio')
        
        
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