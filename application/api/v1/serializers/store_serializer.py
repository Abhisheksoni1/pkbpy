# from apps.common.models import Store
from django.contrib.gis.measure import D
from rest_framework import serializers
from apps.stores.models import Kitchen, StoreAttribute, Store
from .kitchen_serializer import KitchenStoreSerializer,KitchenDistanceStoreSerializer
from libraries.Functions import join_string
from config import settings
from apps.feedback.models import KitchenFeedback
from django.db.models import Avg
from django.db.models import Sum


class StoreBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name']
        # fields = '__all_


class StoreAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAttribute
        fields = ['key', 'value']


class StoreKitchenSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField('get_rating')

    kitchens = serializers.SerializerMethodField('get_kitchen')

    images = serializers.SerializerMethodField('get_image')

    logos = serializers.SerializerMethodField('get_logo')

    total_rates = serializers.SerializerMethodField('get_rate')

    is_open = serializers.SerializerMethodField()

    cost_for_two = serializers.SerializerMethodField('get_cost')

    minimum_order = serializers.SerializerMethodField('get_minimum')

    delivery_time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Store
        fields = ['id', 'name', 'images', 'logos', 'description', 'location', 'address', 'tin_no', 'ratings',
                  'total_rates', 'kitchens', 'minimum_order', 'cost_for_two', 'delivery_time', 'opening_time',
                  'closing_time',
                  'is_open']

    def get_is_open(self, obj):
        return obj.status

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = int(obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = int(obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = int(obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_kitchen(self, obj):
        kitchen = Kitchen.objects.filter(store_id=obj.id, is_deleted=False)
        serializer = KitchenStoreSerializer(kitchen, many=True).data
        return serializer

    def get_image(self, obj):
        if obj.image:
            store_name = join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image
        else:
            directory = None

        return directory

    def get_logo(self, obj):
        if obj.logo:
            store_name = join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.logo
        else:
            directory = None

        return directory

    def get_rating(self, obj):
        try:
            avg_rating = 0.0
            kitchen = Kitchen.objects.filter(store_id=obj.id).values_list('id', flat=True)
            rating = KitchenFeedback.objects.filter(kitchen__in=kitchen).aggregate(rating=Avg('rating'))
            avg_rating = round(rating['rating'], 2)
        except Exception as e:
            print(e)
            avg_rating = 0.0
        return avg_rating

    def get_rate(self, obj):
        try:
            kitchen = Kitchen.objects.filter(store_id=obj.id).values_list('id', flat=True)
            feedback = KitchenFeedback.objects.filter(kitchen__in=kitchen).count()
        except Exception as e:
            feedback = 0
        return feedback


class StoreDistanceSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_image')

    logos = serializers.SerializerMethodField('get_logo')

    ratings = serializers.SerializerMethodField('get_rating')

    total_rates = serializers.SerializerMethodField('get_rate')

    is_open = serializers.SerializerMethodField()

    minimum_order = serializers.SerializerMethodField('get_minimum')

    cost_for_two = serializers.SerializerMethodField('get_cost')

    delivery_time = serializers.SerializerMethodField('get_time')

    kitchens = serializers.SerializerMethodField('get_kitchen')

    is_delivered = serializers.SerializerMethodField('get_delivered')

    class Meta:
        model = Store

        fields = ['id', 'name', 'logos', 'images', 'tag_line', 'ratings', 'description', 'location', 'address',
                  'minimum_order', 'kitchens',
                  'cost_for_two', 'delivery_time', 'total_rates', 'is_open', 'is_delivered']

    def get_delivered(self, obj):
        return True

    def get_logo(self, obj):
        if obj.logo:
            store_name = join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo
        else:
            directory = None

        return directory

    def get_image(self, obj):
        if obj.image:
            store_name = join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image
        else:
            directory = None
        return directory

    def get_rating(self, obj):
        try:
            avg_rating = 0.0
            kitchen = Kitchen.objects.filter(store_id=obj.id).values_list('id', flat=True)
            # count = KitchenFeedback.objects.filter(kitchen__in=kitchen).count()
            rating = KitchenFeedback.objects.filter(kitchen__in=kitchen).aggregate(rating=Avg('rating'))
            if rating['rating']:
                avg_rating = rating['rating']
                avg_rating = round(avg_rating, 2)


        except Exception as e:
            print(e)
            avg_rating = 0.0
        return avg_rating

    def get_rate(self, obj):
        try:
            kitchen = Kitchen.objects.filter(store_id=obj.id).values_list('id', flat=True)
            feedback = KitchenFeedback.objects.filter(kitchen__in=kitchen).count()
        except Exception as e:
            print(e)
            feedback = 0
        return feedback

    def get_is_open(self, obj):
        return obj.status

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = (obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = (obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = (obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_kitchen(self, obj):
        point = self.context.get('point', None)
        if point:
            kitchen = Kitchen.objects.filter(store_id=obj.id, is_deleted=False, location__distance_lte=(point, D(m=7000)))
            # kitchen = Kitchen.objects.filter(store_id=obj.id, is_deleted=False)
        else:
            kitchen = Kitchen.objects.filter(store_id=obj.id, is_deleted=False)
        serializer = KitchenDistanceStoreSerializer(kitchen, many=True).data
        return serializer

    def validate(self, attrs):
        pick_up = self.context['Pick_type']
        if pick_up not in ['DELIVER,SELF-PICKUP']:
            raise serializers.ValidationError('Pick-up type should be eitherDELIVER or SELF-PICKUP')


class StoreDistanceDeliveredSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_image')

    logos = serializers.SerializerMethodField('get_logo')

    ratings = serializers.SerializerMethodField('get_rating')

    total_rates = serializers.SerializerMethodField('get_rate')

    is_open = serializers.SerializerMethodField()

    minimum_order = serializers.SerializerMethodField('get_minimum')

    cost_for_two = serializers.SerializerMethodField('get_cost')

    delivery_time = serializers.SerializerMethodField('get_time')

    kitchens = serializers.SerializerMethodField('get_kitchen')

    is_delivered = serializers.SerializerMethodField('get_delivered')

    class Meta:
        model = Store

        fields = ['id', 'name', 'logos', 'images', 'tag_line', 'ratings', 'description', 'location', 'address',
                  'minimum_order', 'kitchens',
                  'cost_for_two', 'delivery_time', 'total_rates', 'is_open', 'is_delivered']

    def get_delivered(self, obj):
        return False

    def get_logo(self, obj):
        if obj.logo:
            store_name = join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo
        else:
            directory = None

        return directory

    def get_image(self, obj):
        if obj.image:
            store_name = join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image
        else:
            directory = None
        return directory

    def get_rating(self, obj):
        try:
            avg_rating = 0.0
            kitchen = Kitchen.objects.filter(store_id=obj.id).values_list('id', flat=True)
            # count = KitchenFeedback.objects.filter(kitchen__in=kitchen).count()
            rating = KitchenFeedback.objects.filter(kitchen__in=kitchen).aggregate(rating=Avg('rating'))
            if rating['rating']:
                avg_rating = rating['rating']

        except Exception as e:
            print(e)
            avg_rating = 0.0
        return round(avg_rating, 2)

    def get_rate(self, obj):
        try:
            kitchen = Kitchen.objects.filter(store_id=obj.id).values_list('id', flat=True)
            feedback = KitchenFeedback.objects.filter(kitchen__in=kitchen).count()
        except Exception as e:
            print(e)
            feedback = 0
        return feedback

    def get_is_open(self, obj):
        return obj.status

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = (obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = (obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = (obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_kitchen(self, obj):
        kitchen = Kitchen.objects.filter(store_id=obj.id, is_deleted=False)
        serializer = KitchenDistanceStoreSerializer(kitchen, many=True).data
        return serializer

    def validate(self, attrs):
        pick_up = self.context['Pick_type']
        if pick_up not in ['DELIVER,SELF-PICKUP']:
            raise serializers.ValidationError('Pick-up type should be eitherDELIVER or SELF-PICKUP')


class StoreTakeawaySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_image')

    logos = serializers.SerializerMethodField('get_logo')

    ratings = serializers.SerializerMethodField('get_rating')

    total_rates = serializers.SerializerMethodField('get_rate')

    is_open = serializers.SerializerMethodField()

    minimum_order = serializers.SerializerMethodField('get_minimum')

    cost_for_two = serializers.SerializerMethodField('get_cost')

    delivery_time = serializers.SerializerMethodField('get_time')

    kitchens = serializers.SerializerMethodField('get_kitchen')

    is_delivered = serializers.SerializerMethodField('get_delivered')

    class Meta:
        model = Store

        fields = ['id', 'name', 'logos', 'images', 'tag_line', 'ratings', 'description', 'location', 'address',
                  'minimum_order', 'kitchens',
                  'cost_for_two', 'delivery_time', 'total_rates', 'is_open', 'is_delivered']

    def get_delivered(self, obj):
        return True

    def get_logo(self, obj):
        if obj.logo:
            store_name = join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo
        else:
            directory = None

        return directory

    def get_image(self, obj):
        if obj.image:
            store_name = join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image
        else:
            directory = None
        return directory

    def get_rating(self, obj):
        try:
            avg_rating = 0.0
            kitchen = Kitchen.objects.filter(store_id=obj.id).values_list('id', flat=True)
            # count = KitchenFeedback.objects.filter(kitchen__in=kitchen).count()
            rating = KitchenFeedback.objects.filter(kitchen__in=kitchen).aggregate(rating=Avg('rating'))
            if rating['rating']:
                avg_rating = rating['rating']

        except Exception as e:
            print(e)
            avg_rating = 0.0
        return round(avg_rating, 2)

    def get_rate(self, obj):
        try:
            kitchen = Kitchen.objects.filter(store_id=obj.id).values_list('id', flat=True)
            feedback = KitchenFeedback.objects.filter(kitchen__in=kitchen).count()
        except Exception as e:
            print(e)
            feedback = 0
        return feedback

    def get_is_open(self, obj):
        return obj.status

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = (obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = (obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = (obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_kitchen(self, obj):
        point = self.context.get('point', None)
        if point:
            kitchen = Kitchen.objects.filter(store_id=obj.id, is_deleted=False,
                                             location__distance_lte=(point, D(m=20000)))
            # kitchen = Kitchen.objects.filter(store_id=obj.id, is_deleted=False)
        else:
            kitchen = Kitchen.objects.filter(store_id=obj.id, is_deleted=False)
        serializer = KitchenDistanceStoreSerializer(kitchen, many=True).data
        return serializer


    def validate(self, attrs):
        pick_up = self.context['Pick_type']
        if pick_up not in ['DELIVER,SELF-PICKUP']:
            raise serializers.ValidationError('Pick-up type should be eitherDELIVER or SELF-PICKUP')
