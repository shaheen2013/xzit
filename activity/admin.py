from ast import arg
from django.contrib import admin

from activity.models import Post, PostComment, PostLike, Story, PostImage


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'created_at', 'likes']

    def likes(self, *args, **kwargs):
        post_id = args[0].id
        post_likes = PostLike.objects.filter(post_id=post_id).count()
        return post_likes


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'created_at']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'comment']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['story_type', 'media']


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['image_path']
