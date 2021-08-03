from rest_framework import serializers
from apps.common.models import PromoBanner, Store, Kitchen
from .store_serializer import StoreBannerSerializer
from libraries.Functions import join_string
from config import settings
from libraries.Functions import join_string
from config import settings
from apps.discounts.models import PromoCode, PromoCodeAttribute
from datetime import datetime


class BannerSerializer(serializers.ModelSerializer):
    kitchen = serializers.SerializerMethodField('get_user_kitchen')
    images = serializers.SerializerMethodField('get_image')

    class Meta:
        model = PromoBanner
        fields = [
            'id', 'title', 'description', 'images', 'kitchen'
        ]

    def get_user_kitchen(self, obj):
        get_kitchen = Kitchen.objects.get(pk=obj.kitchen_id,is_deleted = False)
        get_kitchen_serializer = StoreBannerSerializer(get_kitchen)
        return get_kitchen_serializer.data

    def get_image(self, obj):
        directory = None
        if obj.image:
            promo_name = join_string(obj.title)
            kitchen_obj = Kitchen.objects.get(id=obj.kitchen_id,is_deleted = False)
            kitchen_name, store_name = join_string(kitchen_obj.name), join_string(kitchen_obj.store.name)

            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
                            'BANNER_DIR'] + promo_name + '/' + \
                        settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image
        return directory


class PromoCodeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_images')

    class Meta:
        model = PromoCode
        fields = ['id', 'title', 'max_discount', 'description', 'minimum_order', 'amount','percentage', 'code', 'image']

    def get_images(self, obj):
        directory = None
        if obj.image:
            promo_name = join_string(obj.title)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['PROMO_CODE_DIR'] + promo_name + '/' + obj.image
        return directory


class PromoDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_images')
    valid_days = serializers.SerializerMethodField('get_time')
    code_detail = serializers.SerializerMethodField('get_detail')

    class Meta:
        model = PromoCode
        fields = ['id', 'title', 'description', 'image', 'max_discount', 'description', 'minimum_order', 'amount','percentage',
                  'code', 'valid_days',
                  'from_date', 'to_date',
                  'from_time', 'to_time','code_detail']

    def get_images(self, obj):
        directory = None
        if obj.image:
            promo_name = join_string(obj.title)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['PROMO_CODE_DIR'] + promo_name + '/' + obj.image
        return directory

    def get_time(self, obj):
        if obj.to_date and obj.from_date:
            delta = (obj.to_date - obj.from_date).days
        else:
            delta=0
        return delta

    def get_detail(self, obj):
        try:
            code_detail = PromoCodeAttribute.objects.filter(code_id=obj.id,is_deleted = False)
            serializers = PromoCodeAttributeSerializer(code_detail, many=True)
            data = serializers.data
        except Exception as e:
            data = None
        return data


class PromoCodeAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCodeAttribute
        fields = ['key']
