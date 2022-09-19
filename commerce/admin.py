from django.contrib import admin
from commerce.models import BusinessType, Ad, AdBanner, AdComment, AdInvitation, AdLike, Reservation

@admin.register(AdInvitation)
class AdInvitationAdmin(admin.ModelAdmin):
       list_display = ['invited_to', 'invited_by','ad', 'status', 'seen']
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
       list_display = ['ad_titile', 'service', 'date_time', 'table', 'table_duration', 'status', 'guest']
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
       list_display = ['title', 'number_of_invites', 'number_of_accepted', 'event_duration']


admin.site.register(BusinessType)
admin.site.register(AdBanner)
admin.site.register(AdComment)
# admin.site.register(AdInvitation)
admin.site.register(AdLike)
