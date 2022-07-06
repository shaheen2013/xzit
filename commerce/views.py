from rest_framework.response import Response
from rest_framework import status
from commerce import serializers, models
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView


class CategoryApiView(ModelViewSet):
    queryset = models.Category.objects.viewable()
    serializer_class = serializers.CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(models.Category, id=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdApiView(ModelViewSet):
    queryset = models.Ad.objects.all()
    serializer_class = serializers.AdSerializer


class AdBannerApiView(ModelViewSet):
    queryset = models.AdBanner.objects.all()
    serializer_class = serializers.AdBannerSerializer

