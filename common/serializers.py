from dataclasses import field, fields
from rest_framework import serializers
from .models import ReportReason,Country,City

class ReportReasonSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields = ('id', 'reason')
        extra_kwargs = {
            'id': {'read_only': True}
        }

class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name','iso_code','phone_number_regx')

class CitySerializers(serializers.ModelSerializer):
    country = CountrySerializers()
    class Meta:
        model = City
        fields =  ('name','country')