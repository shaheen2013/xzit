from rest_framework.response import Response
from rest_framework import status
from commerce import serializers, models
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView


class BusinessTypeApiView(ModelViewSet):
    queryset = models.BusinessType.objects.viewable()
    serializer_class = serializers.BusinessTypeSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(models.BusinessType, id=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdApiView(ModelViewSet):
    queryset = models.Ad.objects.all()
    serializer_class = serializers.AdSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Ad.objects.filter(created_by=self.request.user)


class AdBannerApiView(ModelViewSet):
    queryset = models.AdBanner.objects.all()
    serializer_class = serializers.AdBannerSerializer
    permission_classes = [IsAuthenticated]

