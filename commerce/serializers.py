from rest_framework import serializers
from commerce import models
from django.shortcuts import get_object_or_404


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    parent = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = models.Category
        fields = ('id', 'category_name', 'category_image', 'children', 'parent')

    def create(self, validated_data):
        parent = validated_data.get('parent')
        if parent:
            validated_data.pop('parent')
        instance = models.Category.objects.create(**validated_data)
        instance.save()
        if parent:
            try:
                instance.parent = models.Category.objects.get(id=parent)
                instance.save()
            except:
                pass

        return instance

    def update(self, instance, validated_data):
        parent = validated_data.get('parent')
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.category_image = validated_data.get('category_image', instance.category_image)
        instance.save()

        if parent:
            try:
                instance.parent = models.Category.objects.get(id=parent)
                instance.save()
            except:
                pass
        return instance


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ad
        fields = '__all__'


class AdBannerImageShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdBannerImage
        fields = ('id', 'path')


class AdBannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdBannerImage
        fields = '__all__'


class AdBannerSerializer(serializers.ModelSerializer):
    ad_banner_images = AdBannerImageShowSerializer(many=True)

    # ad = AdSerializer()

    class Meta:
        model = models.AdBanner
        fields = ('id', 'ad', 'ratio', 'ad_banner_images')

    def create(self, validated_data):
        images = []
        if validated_data.get('ad_banner_images'):
            images = validated_data.pop('ad_banner_images')

        instance = models.AdBanner.objects.create(**validated_data)
        instance.save()
        for img in images:
            obj = models.AdBannerImage.objects.create(path=img.get('path'), ad_banner=instance)
            obj.save()

        return instance
