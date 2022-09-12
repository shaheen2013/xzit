from ntpath import realpath
from re import T
from statistics import mode
from django.db import models
from mptt.managers import TreeManager
from xzit.mixins.models import AuthorMixin, TimeStampMixin
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import os 
from xzit.mixins.image_optimizer import reduce_image_size

class BusinessTypeManager(TreeManager):
    def viewable(self):
        queryset = self.get_queryset().filter(level=0)
        return queryset


class BusinessType(MPTTModel, TimeStampMixin):
    name = models.CharField(max_length=255)
    icon = models.ImageField("Type Icon", upload_to="icons/", blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    objects = BusinessTypeManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "business_types"


class Ad(AuthorMixin, TimeStampMixin):
    business_type = models.ForeignKey(BusinessType, blank=True, null=True, on_delete=models.CASCADE, related_name='ad_business_type')
    business_sub_type = models.ManyToManyField(BusinessType,  related_name='ad_business_sub_type')
    company_name = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    parking = models.CharField(max_length=255, null=True, blank=True)
    event_duration = models.CharField(max_length=255, null=True, blank=True)
    event_time = models.DateTimeField(null=True, blank=True)
    event_days = models.IntegerField(null=True, blank=True)
    country_code = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amenties = models.CharField(max_length=255, null=True, blank=True)
    total_shares = models.CharField(max_length=20, default=0, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def total_invites(self):
        return AdInvitation.objects.filter(ad=self.id)
    
    def accepted_invites(self):
        return AdInvitation.objects.filter(ad=self.id, status="accepted")
    
    def number_of_invites(self):
        return self.total_invites().count()
    
    def number_of_accepted(self):
        return self.accepted_invites().count()

    class Meta:
        db_table = "ads"


class Reservation(AuthorMixin, TimeStampMixin):

    status = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    date = models.DateField(auto_created=False, auto_now=False)
    time = models.TimeField(auto_created=False, auto_now=False)
    table = models.CharField(max_length=100, null=True, blank=True)
    table_duration = models.CharField(max_length=50, null=True, blank=True)
    service = models.CharField(max_length=200, null=True, blank=True)
    num_of_guest = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    invited_guest = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

    # for alternavite suggestions
    has_alternavite = models.BooleanField(default=False)
    date_alt = models.DateField(auto_created=False, auto_now=False, null=True, blank=True)
    time_alt = models.TimeField(auto_created=False, auto_now=False, null=True, blank=True)
    table_alt = models.CharField(max_length=100, null=True, blank=True)

    # approval
    marchant_status = models.CharField(max_length=12, choices=status, default='pending', null=True, blank=True)
    user_status = models.CharField(max_length=12, choices=status, default= 'accepted', null=True, blank=True)
    
    class Meta:
        db_table = "reservations"
        
    def guest(self, *args, **kwargs):
        return self.num_of_guest + self.invited_guest
    
    def date_time(self):
        return f'{self.date} {self.time}'
    
    def ad_titile(self):
        return self.ad.title
    

class AdBanner(TimeStampMixin):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='adimage')
    ratio = models.CharField(max_length=255)
    image_path = models.FileField(null=True, blank=True, upload_to="banners/", validators=[FileExtensionValidator(allowed_extensions=["jpg",'png','mp4'])])

    def __str__(self):
        return self.ad.title

    class Meta:
        db_table = "ad_banners"

    def save(self, *args, **kwargs):
        if self.image_path.name is not None:
            name, extension = os.path.splitext(self.image_path.name)
            if extension in ['.jpg','.png','.jpeg']:
                new_image = reduce_image_size(self.image_path)
                self.image_path = new_image
        super().save(*args, **kwargs)



class AdComment(AuthorMixin, TimeStampMixin):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='adcomment')
    comment = models.TextField()

    def __str__(self):
        return self.ad.title

    class Meta:
        db_table = "ad_comments"

User = get_user_model()

class AdInvitation(TimeStampMixin):
    STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    )
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='adinvation')
    referrer_id = models.CharField(max_length=20)
    invited_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='invited')
    invited_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='inviting')
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    seen_at = models.DateTimeField(null=True, blank=True, auto_now=False)

    def __str__(self):
        return self.invited_to.name()

    def seen(self):
        if self.seen_at is None:
            return False 
        else:
            return True
        
    class Meta:
        db_table = "ad_invitations"


class AdLike(AuthorMixin, TimeStampMixin):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='adlike')

    def __str__(self):
        return self.ad.title

    class Meta:
        db_table = "ad_likes"


class AdSave(AuthorMixin, TimeStampMixin):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='adsave')

    def __str__(self):
        return self.ad.title

    class Meta:
        db_table = "ad_save"
