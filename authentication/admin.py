from re import A
from django.contrib import admin

from authentication.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
       list_display = ['username', 'email', 'created_at']