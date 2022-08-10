from requests import request
from rest_framework.response import Response
from rest_framework import status
from commerce import serializers, models
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from authentication.models import User

from rest_framework.parsers import MultiPartParser, FormParser

class BusinessTypeApiView(ModelViewSet):
    queryset = models.BusinessType.objects.viewable()
    serializer_class = serializers.BusinessTypeSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(models.BusinessType, id=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetBussinessTypeApiView(ListAPIView):
    serializer_class = serializers.BusinessTypeSerializer
    queryset = models.BusinessType.objects.all()
    

class SingleBusinessTypeApiView(RetrieveAPIView):
    serializer_class = serializers.BusinessTypeSerializer
    queryset = models.BusinessType.objects.all()
    lookup_field = "id"

    
class AdApiView(ModelViewSet):
    queryset = models.Ad.objects.all()
    serializer_class = serializers.AdSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Ad.objects.filter(created_by=self.request.user.id)

    
class AdReportApiView(CreateAPIView):
    """
        Report to Story
    """
    serializer_class = serializers.AdReportSerializer
    permission_classes = [IsAuthenticated]
    
class SendAdInviteApiView(CreateAPIView):
    """ 
        Send Ad Invitation 
    """
    serializer_class = serializers.CreateInviteSerializer
    permission_classes = [IsAuthenticated]

class AdInvitationUpdateApiView(UpdateAPIView):
    serializer_class = serializers.AdInvitationListSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.AdInvitation.objects.all()
    lookup_field = "id"
    
class AdInvitationsListApiView(ListAPIView):
    """ 
        All ad invitations list request for me. 
    """
    serializer_class = serializers.AdInvitationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.AdInvitation.objects.filter(invited_to=self.request.user)
    
class AdSendedInvitationListApiView(ListAPIView):
    """ 
        All Ad Invitations list I send to other
    """
    serializer_class = serializers.AdInvitationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.AdInvitation.objects.filter(invited_by=self.request.user)


class AdBannerImageCreateApiView(CreateAPIView):
    queryset = models.AdBanner
    serializer_class = serializers.AdBannerImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    
    """********************************************************************************************
                                                    Reservation 
    *********************************************************************************************"""
class ReservationCreateApiView(CreateAPIView):
    """ 
        Create a reservation
    """
    serializer_class = serializers.ReservationCreateSerializer
    permission_classes = [IsAuthenticated]
class UserReservationListApiView(ListAPIView):
    """ 
        User reservation list
    """
    serializer_class = serializers.UserReservationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Reservation.objects.filter(created_by=self.request.user.id)
    
class ReservationDetailApiView(RetrieveAPIView):
    """ 
        Reservation details. 
    """
    
    serializer_class = serializers.ReservationSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Reservation.objects.filter(created_by=self.request.user.id)
    
class ReservationUserUpdateApiView(UpdateAPIView):
    """ 
        Reservation Update. 
    """
    
    serializer_class = serializers.ReservationUpdateSerializer
    lookup_field = "id"
    queryset = models.Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        reservation = get_object_or_404(models.Reservation, id=kwargs.get("id"))
        if request.user.id != reservation.created_by_id:
            return Response({ "details": "You have no permission to update this"}, 400)
        
        return super().update(request, *args, **kwargs)
    
    
class ReservationMerchantUpdateApiView(UpdateAPIView):
    """ 
        Reservation Update. 
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ReservationUpdateSerializer
    queryset = models.Reservation.objects.all()
    lookup_field = "id"
    
    def patch(self, request, *args, **kwargs):
        reservation = get_object_or_404(models.Reservation, id=kwargs.get("id"))
        ad = reservation.ad 
        if ad.created_by_id != request.user.id:
            return Response({ "details": "You have no permission to update this"}, 403)
        return super().partial_update(request, *args, **kwargs)
    
class MerchantReservationListApiView(ListAPIView):
    """ 
    Reservations list for merchant
    """
    serializer_class = serializers.ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        ads = models.Ad.objects.filter(created_by_id__pk=self.request.user.id) 
        return models.Reservation.objects.filter(ad__in=ads)
    

