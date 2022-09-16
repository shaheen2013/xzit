from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ReportReason,Country,City
from rest_framework.filters import SearchFilter
from . models import *
from . import serializers
from rest_framework import generics
from rest_framework import filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView, Response

# Create your views here.
class ReportReasonList(generics.ListAPIView):
    serializer_class = serializers.ReportReasonSerializers
    queryset = ReportReason.objects.all()
    permission_classes = [IsAuthenticated]


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name',]
    filter_backends=(SearchFilter,OrderingFilter)
    
class CountryDetailsView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = serializers.CountryDetailsSerializer
    lookup_field = "name"
    

class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
    filter_backends=(SearchFilter,OrderingFilter)
    

class CitySearchView(APIView):
    def get(self, request, country=None, format=None):
        city = request.GET.get('q', None)
        if city is not None:
            cities = City.objects\
            .filter(name__icontains=city) \
            .filter(country__name=country)
            res_data = serializers.CitySerializer(cities, many=True).data
            return Response(res_data)
        return Response([])
    
class CityDetailsView(APIView):
    def get(self, request, country=None, city=None, format=None):
        if city is not None:
            cities = City.objects\
            .filter(name=city) \
            .filter(country__name=country).first()
            res_data = serializers.CitySerializer(cities).data
            return Response(res_data)
        return Response({})

# # for country List

# class CountryList(generics.ListAPIView):
#     serializer_class = serializers.CountrySerializers
#     queryset = Country.objects.all()
#     permission_classes = [IsAuthenticated]   
#     filter_backends = [SearchFilter]

#     search_fields = ['name']

# # for country  view by name

# class CountryCheckAPIView(generics.RetrieveAPIView):
#     serializer_class = serializers.CountrySerializers
#     queryset = Country.objects.all()
#     filter_backends = [SearchFilter]
#     #lookup_field = 'country'
#     search_fields = ['country']

    
#     # def retrieve(self, request, *args, **kwargs):

#     #     return super().retrieve(request, *args, **kwargs)


# # for City


  
# class CityList(generics.ListAPIView):
#     serializer_class = serializers.CitySerializers
#     queryset = City.objects.all()
#     permission_classes = [IsAuthenticated]
#     filter_backends = [SearchFilter]
#     search_fields = ['name']




# class CityCheckAPIView(generics.RetrieveAPIView):
#     serializer_class = serializers.CitySerializers
#     queryset = City.objects.all()
#     lookup_field = 'name'

#     def retrieve(self, request, *args, **kwargs):
#         # instance = self.queryset.filter()
#         name = self.kwargs.get('name', None)
#         country = self.kwargs.get('country', None)
#         instance = self.queryset.filter(name=name, country__name=country).first()
#         if not instance:
#             raise ValidationError({'details': 'No city/country found with these keywords!', 'status': status.HTTP_404_NOT_FOUND})
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
        

    

    
# class CountryView(generics.ListAPIView):
#     serializer_class = serializers.CountrySerializers
#     queryset = City.objects.all()
#     permission_classes = [IsAuthenticated]
#     filter_backends = [SearchFilter]
#     lookup_field = 'country'
#     search_fields = ['name']








