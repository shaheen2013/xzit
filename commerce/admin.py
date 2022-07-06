from django.contrib import admin
from commerce.models import Category, Ad, AdBanner, AdBannerImage, AdComment, AdInvitation, AdLike


admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(AdBanner)
admin.site.register(AdBannerImage)
admin.site.register(AdComment)
admin.site.register(AdInvitation)
admin.site.register(AdLike)
