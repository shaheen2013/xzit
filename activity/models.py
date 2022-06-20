from django.db import models
from django.contrib.auth import get_user_model

from xzit.mixins.models import TimeStampMixin


# Create your models here.

User = get_user_model()

class Post(TimeStampMixin):
       id = models.AutoField(primary_key=True)
       user_id = models.ForeignKey(User, on_delete=models.CASCADE)
       
       
       class Meta:
              db_table="posts"
       
