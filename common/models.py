from django.db import models
from activity.models import Post, Story
from authentication.models import User
from commerce.models import Ad
from xzit.mixins.models import AuthorMixin, TimeStampMixin 

class Report(TimeStampMixin, AuthorMixin):
       REPORT_TYPES = (
              ('Post', 'post'),
              ('Story', 'story'),
              ('Ad', 'ad'),
              ('User', 'user')
       )
       reason = models.TextField(null=False, blank=False)
       report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
       
       post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
       user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
       story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True, blank=True)
       ad = models.ForeignKey(Ad, on_delete=models.CASCADE, blank=True, null=True)
       
       class Meta:
              db_table = "reports"
       

class SavePostAd(TimeStampMixin, AuthorMixin):
       post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
       ad = models.ForeignKey(Ad, on_delete=models.CASCADE, blank=True, null=True)
       
       