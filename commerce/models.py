from django.db import models
from mptt.managers import TreeManager

from xzit.mixins.models import AuthorMixin, TimeStampMixin
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()


class BusinessTypeManager(TreeManager):
    def viewable(self):
        queryset = self.get_queryset().filter(level=0)
        return queryset


class BusinessType(MPTTModel, TimeStampMixin):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    objects = BusinessTypeManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "business_types"


class Ad(AuthorMixin, TimeStampMixin):
    business_type = models.ForeignKey(BusinessType, blank=True, null=True, on_delete=models.CASCADE)
    #business_sub_type = models.ForeignKey(BusinessType, blank=True, null=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    parking = models.CharField(max_length=255)
    event_duration = models.CharField(max_length=255)
    event_time = models.DateTimeField()
    event_days = models.IntegerField()
    country_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=40)
    description = models.TextField()
    amenties = models.CharField(max_length=255)
    total_shares = models.CharField(max_length=20)
    container_ratio = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "ads"


class AdBanner(TimeStampMixin):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    ratio = models.CharField(max_length=255)

    def __str__(self):
        return self.ad.title

    class Meta:
        db_table = "ad_banners"


class AdBannerImage(TimeStampMixin):
    ad_banner = models.ForeignKey(AdBanner, on_delete=models.CASCADE, related_name='ad_banner_images')
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.ad_banner.ad.title


class AdComment(AuthorMixin, TimeStampMixin):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.ad.title

    class Meta:
        db_table = "ad_comments"


class AdInvitation(TimeStampMixin):
    STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    )
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    referrer_id = models.CharField(max_length=20)
    invited_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='invited')
    invited_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='inviting')
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    seen_at = models.DateTimeField(null=True, blank=True, auto_now=False)

    def __str__(self):
        return self.invited_to.name

    class Meta:
        db_table = "ad_invitations"


class AdLike(AuthorMixin, TimeStampMixin):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    def __str__(self):
        return self.ad.title

    class Meta:
        db_table = "ad_likes"
