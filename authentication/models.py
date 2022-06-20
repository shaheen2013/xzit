from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from xzit.mixins.models import TimeStampMixin


class User(AbstractUser, TimeStampMixin):
    name = models.CharField(max_length=255)
    email_verified_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    country_code = models.CharField(max_length=3, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    
    business_name = models.CharField(max_length=255, null=True, blank=True)
    business_manager = models.CharField(max_length=255, null=True, blank=True)
    business_type = models.CharField(max_length=255, null=True, blank=True)
    business_days = models.CharField(max_length=255, null=True, blank=True)
    amenties = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users'

# TODO: I will pick the architecture down bellow.
#  i always like to break db tables as many pices as possible for better performance
#  but i had to follow the previous dev work for design the db otherwise
#  it will be hard to sync data from the old db to new
# class UserAddress(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#
class UserSocial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

#
# class UserBusiness(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
