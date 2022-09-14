from rest_framework import generics, status
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import ReportReason,Country,City
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .serializers import ReportReasonSerializers,CountrySerializers,CitySerializers
from rest_framework.exceptions import ValidationError

# Create your views here.
class ReportReasonList(generics.ListAPIView):
    serializer_class = serializers.ReportReasonSerializers
    queryset = ReportReason.objects.all()
    permission_classes = [IsAuthenticated]



# for country List

class CountryList(generics.ListAPIView):
    serializer_class = serializers.CountrySerializers
    queryset = Country.objects.all()
    permission_classes = [IsAuthenticated]   
    filter_backends = [SearchFilter]

    search_fields = ['name']

# for country  view by name

class CountryCheckAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.CountrySerializers
    queryset = Country.objects.all()
    filter_backends = [SearchFilter]
    #lookup_field = 'country'
    search_fields = ['country']

    
    # def retrieve(self, request, *args, **kwargs):

    #     return super().retrieve(request, *args, **kwargs)


# for City


  
class CityList(generics.ListAPIView):
    serializer_class = serializers.CitySerializers
    queryset = City.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name']




class CityCheckAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.CitySerializers
    queryset = City.objects.all()
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        # instance = self.queryset.filter()
        name = self.kwargs.get('name', None)
        country = self.kwargs.get('country', None)
        instance = self.queryset.filter(name=name, country__name=country).first()
        if not instance:
            raise ValidationError({'details': 'No city/country found with these keywords!', 'status': status.HTTP_404_NOT_FOUND})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        

    

    
class CountryView(generics.ListAPIView):
    serializer_class = serializers.CountrySerializers
    queryset = City.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    lookup_field = 'country'
    search_fields = ['name']








