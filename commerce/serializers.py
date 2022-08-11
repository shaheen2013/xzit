from rest_framework import serializers
from commerce import models
from common.models import Report
from rest_framework.response import Response

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class BusinessTypeSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    parent = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = models.BusinessType
        fields = ('id', 'name', 'children', 'parent')

    def create(self, validated_data):
        parent = validated_data.get('parent')
        if parent:
            validated_data.pop('parent')
        instance = models.BusinessType.objects.create(**validated_data)
        instance.save()
        if parent:
            try:
                instance.parent = models.BusinessType.objects.get(id=parent)
                instance.save()
            except:
                pass

        return instance

    def update(self, instance, validated_data):
        parent = validated_data.get('parent')
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if parent:
            try:
                instance.parent = models.BusinessType.objects.get(id=parent)
                instance.save()
            except:
                pass
        return instance

class GetBusinessTypesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.BusinessType
        fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        pass



class AdBannerImageShowSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        'id':{'read_only':True},
        'image_path': {'required': True}
    }
    class Meta:
        model = models.AdBanner
        fields = ('ratio', 'image_path')
    
class AdSerializer(serializers.ModelSerializer):
    adimages = AdBannerImageShowSerializer(many=True, read_only=True, source='adimage')
    class Meta:
        model = models.Ad
        fields = '__all__'




class AdBannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdBanner
        fields = ('ad', 'ratio', 'image_path')

    extra_kwargs = {
        'image_path': {'required': True}
    }


class AdBannerSerializer(serializers.ModelSerializer):
    ad_banner_images = AdBannerImageShowSerializer(many=True, read_only=True)
    class Meta:
        model = models.AdBanner
        fields = ('id', 'ad', 'ratio', 'ad_banner_images')

    # def create(self, validated_data):
    #     images = []
    #     if validated_data.get('ad_banner_images'):
    #         images = validated_data.pop('ad_banner_images')

    #     instance = models.AdBanner.objects.create(**validated_data)
    #     instance.save()
    #     for img in images:
    #         obj = models.AdBannerImage.objects.create(path=img.get('file_path'), ad_banner=instance)
    #         obj.save()

    #     return instance
    
class AdReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('reason', 'ad')
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.report_type = "Ad"
        instance.save()
        return instance
    
class CreateInviteSerializer(serializers.ModelSerializer):
    
    extra_kwargs = {
        'referrer_id': {'read_only' : True},
        'invited_by': {'read_only': True}
    }
    class Meta:
        model = models.AdInvitation
        fields  = ['ad', 'invited_to']

    def create(self, validated_data):
        request = self.context.get('request')
        if request is not None: 
            user = request.user 
            validated_data['invited_by'] = user 
            validated_data['referrer_id'] = user.id 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class AdInvitationListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AdInvitation
        fields = "__all__"

class InviteDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AdInvitation
    
    
class ReservationSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(initial=False)

    extra_kwargs = {
        'number_of_accepted': {'read_only' : True},
        'ad_details': {'read_only' : True},
    }
    class Meta: 
        model = models.Reservation
        fields = ('id','ad', 'date', 'service', 'time', 'table', 'table_duration', 'status', 'guest')
        
class ReservationCreateSerializer(ReservationSerializer):
    extra_kwargs = {
        'created_at': {'read_only' : True},
        'created_by': {'read_only': True},
        'status': {'read_only': True}
    }
class UserReservationListSerializer(ReservationSerializer):
    extra_kwargs = {
        'created_at': {'read_only' : True},
        'created_by': {'read_only': True},
        'status': {'read_only': True},
    } 

class ReservationDetailsSerializer(ReservationSerializer):
    extra_kwargs = {
        'created_at': {'read_only' : True},
        'created_by': {'read_only': True}
    } 
    
class ReservationUpdateSerializer(ReservationSerializer):
    extra_kwargs = {
        'created_at': {'read_only' : True},
        'created_by': {'read_only': True }
    }