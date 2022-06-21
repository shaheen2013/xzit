from ast import arg
from django.contrib import admin

from activity.models import Post, PostLike

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
