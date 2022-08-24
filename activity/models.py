from pyexpat import model
from django.db import models
from xzit.mixins.models import AuthorMixin, TimeStampMixin
from django.core.validators import FileExtensionValidator
import uuid

# Create your models here.
class Post(TimeStampMixin, AuthorMixin):
       description = models.TextField(null=True, blank=True)
       total_shares = models.IntegerField(default=0)
       container_ratio = models.IntegerField(default=0)
       location = models.CharField(max_length=200, null=True, blank=True)
       
       class Meta:
              db_table="posts"
              ordering = ('-created_at',)
              
       def __str__(self):
              return f"{self.created_by}"

              
              
class PostLike(TimeStampMixin, AuthorMixin):
       post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postlike')
       
       
       class Meta:
              db_table="like_posts"
              
class PostComment(TimeStampMixin, AuthorMixin):
       comment = models.TextField()
       post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postcomment')
       
       class Meta: 
              db_table = "comment_posts"
              
              
class PostSave(TimeStampMixin, AuthorMixin):
       post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postSave')
       
       class Meta:
              db_table = "save_posts"

class PostShare(TimeStampMixin, AuthorMixin):
       post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_share')
       
       
              
              
class Story(TimeStampMixin, AuthorMixin):
       TYPE_CHOICES = (
              ('image', 'Image'),
              ('video', 'Video')
       )
       story_type = models.CharField(max_length=10, default=TYPE_CHOICES[1], choices=TYPE_CHOICES)
       media = models.FileField(upload_to='stories/', validators=[FileExtensionValidator(allowed_extensions=["jpg",'png','mp4'])])
       view = models.CharField(max_length = 255, null=True, blank=True)
       views_count = models.IntegerField(default=0)
       story_time = models.DateTimeField(auto_now=True)

       class Meta:
              db_table = "stories"
              ordering = ('-created_at',)
              
              
class StoryViewer(TimeStampMixin, AuthorMixin):
       story = models.ForeignKey(Story, on_delete=models.CASCADE)
       
       class Meta:
              db_table = "story_viewers"




from PIL import Image
from io import BytesIO
from django.core.files import File
import os 

class PostImage(TimeStampMixin, AuthorMixin):
       post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postimage')
       image_path = models.FileField(null=True, blank=True, upload_to="posts/", validators=[FileExtensionValidator(allowed_extensions=["jpg",'png','mp4','jpeg'])])


       def save(self, *args, **kwargs):
              name, extension = os.path.splitext(self.image_path.name)
              if extension in ['.jpg','.png','.jpeg']:
                     new_image = self.reduce_image_size(self.image_path)
                     self.image_path = new_image
              super().save(*args, **kwargs)

       def reduce_image_size(self, profile_pic):
              prepix = uuid.uuid4().hex[:].upper()
              name, extension = os.path.splitext(profile_pic.name)
              if extension == '.jpg':
                     format = 'jpeg'
              else:
                     format = 'png'
              img = Image.open(profile_pic)
              thumb_io = BytesIO()
              img.save(thumb_io, format=format, quality=50)
              new_image = File(thumb_io, name=prepix+extension)
              return new_image
