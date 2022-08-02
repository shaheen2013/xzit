from django.contrib import admin
from commerce.models import BusinessType, Ad, AdBanner, AdBannerImage, AdComment, AdInvitation, AdLike

@admin.register(AdInvitation)
class AdInvitationAdmin(admin.ModelAdmin):
       list_display = ['invited_to', 'invited_by','ad', 'status', 'seen']


admin.site.register(BusinessType)
admin.site.register(Ad)
admin.site.register(AdBanner)
admin.site.register(AdBannerImage)
admin.site.register(AdComment)
# admin.site.register(AdInvitation)
admin.site.register(AdLike)
