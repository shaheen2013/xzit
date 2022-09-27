from django.contrib import admin
from .models import ReportReason,Friends,BlockFriends

# Register your models here.

admin.site.register(ReportReason)
admin.site.register(Friends)
admin.site.register(BlockFriends)
# class BlockFriendsAdmin(admin.ModelAdmin):
#     list_display = ("user", "id",)

# admin.site.register(BlockFriends, BlockFriendsAdmin)
