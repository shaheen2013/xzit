from django.contrib import admin
from .models import ReportReason, Country, City

# Register your models here.

admin.site.register(ReportReason)

class CityInline(admin.TabularInline):
    model = City

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code', 'phone_number_regx']
    inlines = [CityInline]
