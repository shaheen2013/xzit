from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from xzit.mixins.models import TimeStampMixin
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

AUTH_PROVIDERS = {'facebook': 'Facebook','google': 'Google', 'username': 'Username'}


class User(AbstractUser, TimeStampMixin):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    email_verified_at = models.DateTimeField(auto_now_add=True)
    
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, null=True, blank=True)
    
    phone = models.CharField(max_length=40, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)

    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('username'))

    country_code = models.CharField(max_length=3, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)

    business_name = models.CharField(max_length=255, null=True, blank=True)
    business_manager = models.CharField(max_length=255, null=True, blank=True)
    business_type = models.CharField(max_length=255, null=True, blank=True)
    business_sub_type = models.CharField(max_length=255, null=True, blank=True)
    business_days = models.CharField(max_length=255, null=True, blank=True)
    business_hours = models.CharField(max_length=255, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)
    
    bio = models.TextField(null=True, blank=True)
    
    amenties = models.CharField(max_length=255, null=True, blank=True)
    
    device_type = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'users'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        
    def name(self):
        return f"{self.first_name} {self.last_name}" 
        
        
    def role(self):
        group = self.groups.first()
        if group is not None:
            return group.name
        return 'No Role'


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="XZIT Backend"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
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
