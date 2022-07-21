from re import A
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import User

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_image', 'cover_image', 'gender', 'birth_date', 'country_code', 'country', 'city', 'address', 'latitude')
        }),
        ('Business info', {
            'fields': ('business_name', 'business_manager', 'business_type', 'business_days', 'amenties')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'phone', 'password1', 'password2')
        }),
    )

    # def save_model(self, request, obj, form, change):
    #     try:
    #         super(UserAdmin, self).save_model(request, obj, form, change)
    #     except:
    #         obj.password = hashers.make_password(request.POST['password'])
    #         super(UserAdmin, self).save_model(request, obj, form, change)
