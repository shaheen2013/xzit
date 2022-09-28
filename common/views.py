
from django.shortcuts import render
from rest_framework import generics
from commerce.models import User
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
class ReportReasonList(generics.ListAPIView):
    serializer_class = serializers.ReportReasonSerializers
    queryset = ReportReason.objects.all()
    permission_classes = [IsAuthenticated]
    
    
@api_view(['POST'])  
def friend_add(request):
    data = request.data
    friend_exist = Friends.objects.filter(user=data['user']).first()
    block_exist = BlockFriends.objects.filter(user=data['user']).first()
    if block_exist:
        return Response("You Can't Add friend to a blocked person.")
    if friend_exist:
        return Response(serializers.FriendSerializers(friend_exist).data)
    serializer=serializers.FriendSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])  
def friend_list(request):
    # if request.method == "GET":
    serializer = serializers.FriendSerializers(Friends.objects.all(), many=True)
    return Response(serializer.data)

@api_view(['GET'])  
def block_list(request):
    serializer = serializers.BlockFriendSerializers(BlockFriends.objects.all(), many=True)
    return Response(serializer.data)
    
@api_view(['POST'])  
def add_block(request):
    data = request.data
    friend_exist = Friends.objects.filter(user=data['user']).first()
    block_exist = BlockFriends.objects.filter(user=data['user']).first()
    if block_exist:
        return Response(serializers.BlockFriendSerializers(friend_exist).data)
    if friend_exist:
        friend_exist.delete()
    serializer=serializers.BlockFriendSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(serializer.data)

    
        