
from rest_framework import serializers
from activity.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('description', 'created_by')