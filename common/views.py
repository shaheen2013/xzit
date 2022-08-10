from django.shortcuts import render
from rest_framework import generics
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import ReportReason

# Create your views here.
class ReportReasonList(generics.ListAPIView):
    serializer_class = serializers.ReportReasonSerializers
    queryset = ReportReason.objects.all()
    permission_classes = [IsAuthenticated]