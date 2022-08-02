from rest_framework.response import Response
from rest_framework import status
from commerce import serializers, models
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView

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


class AdBannerApiView(ModelViewSet):
    queryset = models.AdBanner.objects.all()
    serializer_class = serializers.AdBannerSerializer
    permission_classes = [IsAuthenticated]
    
    
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
    
    
    
    

