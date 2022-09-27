from rest_framework import serializers
from .models import ReportReason,Friends,BlockFriends

class ReportReasonSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields = ('id', 'reason')
        extra_kwargs = {
            'id': {'read_only': True}
        }
        
class FriendSerializers(serializers.ModelSerializer):
    def getUsername(self, obj):
        return obj.user.username
    friend_name = serializers.SerializerMethodField("getUsername")
    class Meta:
        model = Friends
        fields = ('id', 'user','friend_name')
        
class BlockFriendSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = BlockFriends
        fields = ('id', 'user','username')
        

