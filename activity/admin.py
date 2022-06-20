from django.contrib import admin

from activity.models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
       list_display = ['created_by', 'created_at']
