from re import A
from django.contrib import admin
from django import forms
from django.contrib.auth import hashers

from authentication.models import User

# Register your models here.
from xzit import settings


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email', 'created_at']

    def save_model(self, request, obj, form, change):
        try:
            print(hashers.identify_hasher(request.POST['password']))
            super(UserAdmin, self).save_model(request, obj, form, change)
        except:
            obj.password = hashers.make_password(request.POST['password'])
            super(UserAdmin, self).save_model(request, obj, form, change)
