from django.shortcuts import render
from rest_framework import generics
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import ReportReason,Country,City
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .serializers import ReportReasonSerializers,CountrySerializers,CitySerializers


# Create your views here.
class ReportReasonList(generics.ListAPIView):
    serializer_class = serializers.ReportReasonSerializers
    queryset = ReportReason.objects.all()
    permission_classes = [IsAuthenticated]



# for country 

class CountryList(generics.ListAPIView):
    serializer_class = serializers.CountrySerializers
    queryset = Country.objects.all()
   # permission_classes = [IsAuthenticated]   
 #   filter_backends = [SearchFilter]

  #  search_fields = ['name']
    
class CountryListSearch(generics.ListAPIView):
    serializer_class = serializers.CountrySerializers
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        queryset = Country.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


# for City

  
class CityList(generics.ListAPIView):
    serializer_class = serializers.CitySerializers
    queryset = City.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    

    search_fields = ['name']
    

    
    