from pyexpat import model
from django.db import models
from xzit.mixins.models import AuthorMixin, TimeStampMixin
from django.core.validators import FileExtensionValidator


# Create your models here.
class Post(TimeStampMixin, AuthorMixin):
       description = models.TextField(null=True, blank=True)
       total_shares = models.IntegerField(default=0)
       container_ratio = models.IntegerField(default=0)
       location = models.CharField(max_length=200, null=True, blank=True)
       
       class Meta:
              db_table="posts"
              
       def __str__(self):
              return f"{self.created_by}"

              
              
class PostLike(TimeStampMixin, AuthorMixin):
       post = models.ForeignKey(Post, on_delete=models.CASCADE)
       
       
       class Meta:
              db_table="like_posts"
              
class PostComment(TimeStampMixin, AuthorMixin):
       comment = models.TextField()
       post = models.ForeignKey(Post, on_delete=models.CASCADE)
       
       class Meta: 
              db_table = "comment_posts"
              
              
class PostSave(TimeStampMixin, AuthorMixin):
       post = models.ForeignKey(Post, on_delete=models.CASCADE)
       
       class Meta:
              db_table = "save_posts"
              
              
class Story(TimeStampMixin, AuthorMixin):
       TYPE_CHOICES = (
              ('image', 'Image'),
              ('video', 'Video')
       )
       story_type = models.CharField(max_length=10, default=TYPE_CHOICES[1], choices=TYPE_CHOICES)
       media = models.CharField(max_length=255, null=True, blank=True)
       view = models.CharField(max_length = 255, null=True, blank=True)
       views_count = models.IntegerField(default=0)
       story_time = models.DateTimeField(auto_now=True)

       class Meta:
              db_table = "stories"
              
              
class StoryViewer(TimeStampMixin, AuthorMixin):
       story = models.ForeignKey(Story, on_delete=models.CASCADE)
       
       class Meta:
              db_table = "story_viewers"




class PostImage(TimeStampMixin, AuthorMixin):
       post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postimage')
       image_path = models.FileField(null=True, blank=True, upload_to="posts/", validators=[FileExtensionValidator(allowed_extensions=["jpg",'png','mp4'])])
