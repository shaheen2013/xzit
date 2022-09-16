from cgitb import reset
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
    queryset = models.BusinessType.objects.filter(parent=None).all()
    

class SingleBusinessTypeApiView(RetrieveAPIView):
    serializer_class = serializers.BusinessTypeSerializer
    queryset = models.BusinessType.objects.all()
    lookup_field = "id"

    
class AdApiView(ModelViewSet):
    queryset = models.Ad.objects.select_related('business_type').prefetch_related('adimage', 'business_sub_type').all()
    serializer_class = serializers.AdSerializerGet
    permission_classes = [IsAuthenticated]
    # parser_classes = [FormParser]

    def get_serializer_class(self):
        if self.request.method in ['POST','PUT', 'PATCH']:
            return serializers.AdSerializerPostPutPatch
        return super().get_serializer_class()
        
    
    def get_queryset(self):
        return models.Ad.objects.filter(created_by=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for image in instance.adimage.all():
            image.image_path.delete(False)
        return super().destroy(request, *args, **kwargs)


class AdCommentCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AdCommentSerializerPost


class AdLikeCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AdLikeSerializerPost

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'details' : 'Ad Liked', 'status': status.HTTP_201_CREATED})


class AdSaveCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AdSaveSerializerPost

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'details' : 'Ad Saved', 'status': status.HTTP_201_CREATED})



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

    # overriding create methode for custome Response
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        ad = request.data.get('ad')
        adinvitation = models.AdInvitation.objects.filter(ad=ad)
        return Response(serializers.CreateInviteSuccessSerializer(adinvitation, many=True, context={'request': request}).data)
        # adInvitation = models.AdInvitation.objects.filter(ad=request.data['ad'])
        

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

    # Creating new authentication class for Merchant by extending IsAuthenticated

class IsAuthenticatedMerchant(IsAuthenticated):
    """
    Allows access only to authenticated merchant group users.
    """
    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and request.user.groups.filter(name="merchant").exists())


class IsAuthenticatedUser(IsAuthenticated):
    """
    Allows access only to authenticated merchant group users.
    """
    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and request.user.groups.filter(name="user").exists())


class ReservationCreateApiView(CreateAPIView):
    """ 
        Create a reservation
    """
    serializer_class = serializers.ReservationCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['invited_guest'] = models.AdInvitation.objects.filter(ad=request.data['ad'], status='accepted', invited_by=request.user).count()
        return super().create(request, *args, **kwargs)

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


class ReservationMerchantSetAlternative(UpdateAPIView):
    """ 
        Reservation Update. 
    """
    permission_classes = [IsAuthenticatedMerchant]
    serializer_class = serializers.ReservationSetAltSerializer
    queryset = models.Reservation.objects.all()
    lookup_field = "id"
    
    def patch(self, request, *args, **kwargs):
        reservation = get_object_or_404(models.Reservation, id=kwargs.get("id"))
        ad = reservation.ad 
        if ad.created_by_id != request.user.id:
            return Response({ "details": "You have no permission to update this"}, 403)
        return super().partial_update(request, *args, **kwargs)


class AlternativeReservationMerchantStatus(UpdateAPIView):
    permission_classes = [IsAuthenticatedMerchant]
    serializer_class = serializers.AlternativeReservationStatusMerchantSerializer
    queryset = models.Reservation.objects.all()
    lookup_field = "id"


class AlternativeReservationUserStatus(UpdateAPIView):
    permission_classes = [IsAuthenticatedUser]
    serializer_class = serializers.AlternativeReservationStatusUserSerializer
    queryset = models.Reservation.objects.all()
    lookup_field = "id"



    
class MerchantReservationListApiView(ListAPIView):
    """ 
    Reservations list for merchant
    """
    serializer_class = serializers.ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        ads = models.Ad.objects.filter(created_by_id__pk=self.request.user.id) 
        return models.Reservation.objects.filter(ad__in=ads)


class MerchantAltReservationListApiView(ListAPIView):
    """ 
    Reservations list for merchant
    """
    serializer_class = serializers.ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        ads = models.Ad.objects.filter(created_by_id__pk=self.request.user.id) 
        return models.Reservation.objects.filter(ad__in=ads, has_alternavite=True, marchant_status='pending')

class UserAltReservationListApiView(ListAPIView):
    """ 
        User reservation list
    """
    serializer_class = serializers.UserReservationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Reservation.objects.filter(created_by=self.request.user.id, has_alternavite=True, user_status='pending')

        