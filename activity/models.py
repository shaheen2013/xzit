from django.db import models

from xzit.mixins.models import AuthorMixin, TimeStampMixin


# Create your models here.
class Post(TimeStampMixin, AuthorMixin):
       description = models.TextField(null=True, blank=True)
       total_shares = models.IntegerField(default=0)
       container_ratio = models.IntegerField(default=0)
       
       
       class Meta:
              db_table="posts"
       
