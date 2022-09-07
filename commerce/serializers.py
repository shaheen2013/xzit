
from dataclasses import field
from statistics import mode
from urllib import request
from rest_framework import serializers
from authentication.serializers import UserProfileSerializer
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
        fields = ('id', 'name', 'icon', 'children', 'parent')

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
        fields = ('id', 'name', 'icon')


class AdBannerImageShowSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        'id':{'read_only':True},
        'image_path': {'required': True}
    }
    class Meta:
        model = models.AdBanner
        fields = ('ratio', 'image_path')


class AdCommentSerializerGet(serializers.ModelSerializer):
    created_by = UserProfileSerializer()
    class Meta:
        model = models.AdComment
        fields = ['comment', 'created_by']

class AdCommentSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = models.AdComment
        fields = ['ad', 'comment']

class AdLikeSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = models.AdLike
        fields = ['ad', 'created_by']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        ad = validated_data.get('ad')
        userAdLike = self.Meta.model.objects.filter(created_by=user, ad_id=ad.id).first()
        if userAdLike is not None:
            userAdLike.delete()
            return userAdLike
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class AdSaveSerializerGet(serializers.ModelSerializer):
    created_by = UserProfileSerializer()
    class Meta:
        model = models.AdSave
        fields = ['ad', 'created_by']

class AdSaveSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = models.AdSave
        fields = ['ad', 'created_by']
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        ad = validated_data.get('ad')
        userAdSave = self.Meta.model.objects.filter(created_by=user, ad_id=ad.id).first()
        if userAdSave is not None:
            userAdSave.delete()
            return userAdSave
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    
class AdSerializerGet(serializers.ModelSerializer):
    business_type = GetBusinessTypesSerializer(read_only=True)
    business_sub_type = GetBusinessTypesSerializer(many=True, read_only=True)
    adimages = AdBannerImageShowSerializer(many=True, read_only=True, source='adimage')
    created_by = UserProfileSerializer()
    ad_like = serializers.SerializerMethodField(method_name='count_likes')
    ad_comment = AdCommentSerializerGet(many=True, source='adcomment')
    ad_save = AdSaveSerializerGet(many=True, source='adsave')

    def count_likes(self, instance: models.Ad):
        return instance.adlike.all().count()
    
    # def get_comments(self, instance: models.Ad):
    #     comment = instance.adcomment.all()
    #     serializer = AdCommentSerializerGet(comment, many=True)
    #     return serializer.data
    
    # def get_saved_ad(self, instance: models.Ad):
    #     request = self.context.get('request')
    #     comment = instance.adsave.filter(created_by=request.user)
    #     serializer = AdSaveSerializerGet(comment, many=True)
    #     return serializer.data

    class Meta:
        model = models.Ad
        fields = '__all__'


class AdSerializerPostPutPatch(serializers.ModelSerializer):
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

class CreateInviteSuccessSerializer(serializers.ModelSerializer):
    invited_to = UserProfileSerializer()
    class Meta:
        model = models.AdInvitation
        fields = ['ad', 'invited_to', 'created_at']

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
        fields = ('id','ad', 'date', 'service', 'time', 'table', 'table_duration', 'status', 'guest', 'alternative_suggestion', 'suggestion_status')
        
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


class ReservationAproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ['status', 'alternative_suggestion']