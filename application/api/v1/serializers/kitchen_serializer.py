from apps.stores.models import Kitchen, Category, KitchenAttribute
from rest_framework import serializers
from .category_serializer import KitchenCategorySerializer
from apps.feedback.models import KitchenFeedback
from apps.stores.models import Item
from django.utils import timezone
from libraries.Functions import join_string
from config import settings
from django.db.models import Avg
from apps.feedback.models import KitchenFeedback

from libraries.Functions import time_check
class KitchenDistanceStoreSerializer(serializers.ModelSerializer):
    # categories = serializers.SerializerMethodField('get_category')

    ratings = serializers.SerializerMethodField('get_rating')

    total_rates = serializers.SerializerMethodField('get_rate')

    is_open = serializers.SerializerMethodField()

    minimum_order = serializers.SerializerMethodField('get_minimum')

    cost_for_two = serializers.SerializerMethodField('get_cost')

    delivery_time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Kitchen
        fields = ['id', 'name','address', 'ratings', 'total_rates', 'opening_time', 'closing_time', 'minimum_order', 'location',
                  'cost_for_two', 'delivery_time', 'is_open']

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = int(obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_rate(self, obj):
        return KitchenFeedback.objects.filter(kitchen_id=obj.id).count()

    def get_is_open(self, obj):
        if obj.status:
            status = time_check(obj)
            return status
        else:
            return obj.status

    # def get_category(self, obj):
    #     category = Category.objects.filter(kitchen_id=obj.id, is_deleted=False)
    #     serializer = KitchenCategorySerializer(category, many=True).data
    #     return serializer

    def get_rating(self, obj):
        feedback = KitchenFeedback.objects.filter(kitchen_id=obj.id).aggregate(rating=Avg('rating'))
        if feedback['rating']:
            return float("%.2f" % feedback['rating'])
        else:
            return 0.0

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


class KitchenStoreSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField('get_category')

    ratings = serializers.SerializerMethodField('get_rating')

    total_rates = serializers.SerializerMethodField('get_rate')

    is_open = serializers.SerializerMethodField()

    minimum_order = serializers.SerializerMethodField('get_minimum')

    cost_for_two = serializers.SerializerMethodField('get_cost')

    delivery_time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Kitchen
        fields = ['id', 'name', 'ratings', 'total_rates', 'categories', 'opening_time', 'closing_time', 'minimum_order',
                  'cost_for_two', 'delivery_time', 'is_open']

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = int(obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_rate(self, obj):
        return KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).count()

    def get_is_open(self, obj):
        if obj.status:
            status = time_check(obj)
            return status
        else:
            return obj.status

    def get_category(self, obj):
        category = Category.objects.filter(kitchen_id=obj.id, is_deleted=False)
        serializer = KitchenCategorySerializer(category, many=True).data
        return serializer

    def get_rating(self, obj):
        feedback = KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).aggregate(rating=Avg('rating'))
        if feedback['rating']:
            return ("%.2f" % feedback['rating'])
        else:
            return 0.0

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = int(obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = int(obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost


class KitchenDetailSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField('get_rating')
    total_rates = serializers.SerializerMethodField('get_rate')
    categories = serializers.SerializerMethodField('get_category')
    # logos = serializers.SerializerMethodField('get_logo')
    images = serializers.SerializerMethodField('get_image')
    is_open = serializers.SerializerMethodField()
    minimum_order = serializers.SerializerMethodField('get_minimum')
    cost_for_two = serializers.SerializerMethodField('get_cost')
    delivery_time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Kitchen
        fields = ['id', 'name', 'images', 'ratings', 'total_rates', 'tag_line', 'location',
                  'address',
                  'categories', 'is_open', 'minimum_order', 'cost_for_two', 'delivery_time', 'delivery_charges',
                  'packing_charges']

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = int(obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_is_open(self, obj):
        if obj.status:
            status = time_check(obj)
            return status
        else:
            return obj.status


    def get_rate(self, obj):
        return KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).count()

    def get_rating(self, obj):

        feedback = KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).aggregate(rating=Avg('rating'))
        if feedback['rating']:
            return ("%.2f" % feedback['rating'])
        else:
            return None

    def get_category(self, obj):
        category = Category.objects.filter(kitchen_id=obj.id, is_deleted=False)
        serializer = KitchenCategorySerializer(category, many=True).data
        return serializer

    def get_logo(self, obj):
        if obj.logo_thumb:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo_thumb
        else:
            directory = None

        return directory

    def get_image(self, obj):
        if obj.image_thumb:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image_thumb
        else:
            directory = None

        return directory

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = int(obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = int(obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost


class KitchenFeedbackSerializer(serializers.ModelSerializer):
    kitchen_id = serializers.IntegerField(required=True)
    message = serializers.CharField(required=True, max_length=1000)
    rating = serializers.IntegerField(required=True)

    class Meta:
        model = KitchenFeedback
        fields = ['id', 'kitchen_id', 'message', 'rating']

    def create(self, validated_data):

        return KitchenFeedback.objects.create(**validated_data, created_on=timezone.now())

    def validate_kitchen_id(self, value):
        if not value:
            raise serializers.ValidationError('Kitchen-id is required.')
        try:
            Kitchen.objects.get(id=int(value))
        except Exception as e:
            raise serializers.ValidationError('Kitchen-id does not exist.')
        return value

    def validate_message(self, value):
        if not value:
            raise serializers.ValidationError('Message is required')

        return value

    def validate_rating(self, value):
        if not value:
            raise serializers.ValidationError('rating is required field')
        if int(value) > 5:
            raise serializers.ValidationError('rating should be integer field and less than 5')
        return value


class KitchenSearchSerializer(serializers.ModelSerializer):
    # key_word = serializers.CharField(required=True, max_length=20)
    images = serializers.SerializerMethodField('get_image')
    is_open = serializers.SerializerMethodField()
    logos = serializers.SerializerMethodField('get_logo')
    ratings = serializers.SerializerMethodField('get_rating')
    total_rates = serializers.SerializerMethodField('get_rate')
    minimum_order = serializers.SerializerMethodField('get_minimum')
    cost_for_two = serializers.SerializerMethodField('get_cost')
    delivery_time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Kitchen
        fields = ['id', 'name', 'logos', 'images', 'ratings', 'total_rates', 'tag_line', 'description', 'location',
                  'address',
                  'is_open', 'minimum_order', 'cost_for_two', 'delivery_time', 'opening_time', 'closing_time',
                  'delivery_charges']

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = int(obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_rate(self, obj):
        return KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).count()

    def get_logo(self, obj):
        if obj.logo_thumb:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo_thumb
        else:
            directory = None

        return directory

    def get_image(self, obj):
        if obj.image_thumb:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image_thumb
        else:
            directory = None

        return directory

    def get_rating(self, obj):

        feedback = KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).aggregate(rating=Avg('rating'))

        if feedback['rating']:
            return ("%.2f" % feedback['rating'])
        else:
            return None

    def get_is_open(self, obj):
        if obj.status:
            status = time_check(obj)
            return status
        else:
            return obj.status

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = int(obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = int(obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost


class ItemSearchSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_images')
    base_price = serializers.SerializerMethodField('get_base_prices')
    kitchen_name = serializers.SerializerMethodField('get_kitchen')
    kitchen_id = serializers.SerializerMethodField('get_id')
    kitchen_location = serializers.SerializerMethodField('get_loc')

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'short_description', 'food_type', 'image', 'base_price', 'kitchen_id',
                  'kitchen_location',
                  'kitchen_name', 'is_offer_active', 'is_variant', 'is_outof_stock']

    def get_loc(self, obj):
        return str(obj.category.kitchen.location)

    def get_kitchen(self, obj):
        return obj.category.kitchen.name

    def get_id(self, obj):
        return obj.category.kitchen.id

    def get_base_prices(self, obj):
        int_base = 0
        if obj.base_price:
            int_base = int(obj.base_price)
        return int_base

    def get_images(self, obj):

        if obj.image_thumb:
            store_name, kitchen_name, category_name, item_name = join_string(obj.category.kitchen.store.name), \
                                                                 join_string(obj.category.kitchen.name), join_string(
                obj.category.name), join_string(obj.name)

            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
                            'CATEGORY_DIR'] + category_name + '/' + \
                        settings.CUSTOM_DIRS['ITEM_DIR'] + item_name + '/' + settings.CUSTOM_DIRS[
                            'IMAGE_DIR'] + obj.image_thumb
        else:
            directory = None
        return directory


class kitchenStatusSerial(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField('get_is_opens')

    class Meta:
        model = Kitchen
        fields = ['id','is_open']

    def get_is_opens(self, obj):
        if obj.status:
            status = time_check(obj)
            print('status',status)
            return status
        else:
            return obj.status


class KitchenCategoryCountSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField('get_rating')
    categories = serializers.SerializerMethodField('get_category')
    logos = serializers.SerializerMethodField('get_logo')
    images = serializers.SerializerMethodField('get_image')
    is_open = serializers.SerializerMethodField()
    total_rates = serializers.SerializerMethodField('get_rate')
    minimum_order = serializers.SerializerMethodField('get_minimum')
    cost_for_two = serializers.SerializerMethodField('get_cost')
    delivery_time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Kitchen
        fields = ['id', 'name', 'logos', 'images', 'tag_line', 'description', 'location', 'address', 'ratings',
                  'total_rates',
                  'categories', 'is_open', 'minimum_order', 'cost_for_two', 'delivery_time', 'cod_limit']

    def get_rating(self, obj):

        feedback = KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).aggregate(rating=Avg('rating'))

        if feedback['rating']:
            return ("%.2f" % feedback['rating'])
        else:
            return None

    def get_category(self, obj):
        dict = []
        category = Category.objects.filter(kitchen_id=obj.id, is_deleted=False)
        for category in category:
            item = Item.objects.filter(category_id=category.id, is_deleted=False)
            dict.append({'id': category.id, 'name': category.name, 'number_of_items': len(item)})
        return dict

    def get_logo(self, obj):
        if obj.logo_image:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo_image
        else:
            directory = None

        return directory

    def get_image(self, obj):
        if obj.image_thumb:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image_thumb
        else:
            directory = None

        return directory

    def get_is_open(self, obj):
        if obj.status:
            status = time_check(obj)
            return status
        else:
            return obj.status

    def get_rate(self, obj):
        return KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).count()

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = int(obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = int(obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = int(obj.delivery_time)
        else:
            int_time = 0
        return int_time


class KitchenSearchratingSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_kitchen')
    name = serializers.SerializerMethodField('get_kitchen_names')
    image = serializers.SerializerMethodField('get_kitchen_images')
    is_open = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField('get_rating')
    total_rates = serializers.SerializerMethodField('get_rate')
    minimum_order = serializers.SerializerMethodField('get_minimum')
    cost_for_two = serializers.SerializerMethodField('get_cost')
    delivery_time = serializers.SerializerMethodField('get_time')
    tag_line = serializers.SerializerMethodField('get_tag')
    description = serializers.SerializerMethodField('get_descriptions')
    address = serializers.SerializerMethodField('get_addresses')
    opening_time = serializers.SerializerMethodField('get_opening_times')
    closing_time = serializers.SerializerMethodField('get_closing_times')

    class Meta:
        model = KitchenFeedback
        fields = ['id', 'name', 'image', 'rating', 'is_open', 'ratings', 'total_rates', 'tag_line',
                  'minimum_order', 'cost_for_two', 'delivery_time', 'description', 'address', 'opening_time',
                  'closing_time']

    def get_descriptions(self, obj):
        return obj.kitchen.description

    def get_opening_times(self, obj):
        return obj.kitchen.opening_time

    def get_closing_times(self, obj):
        return obj.kitchen.closing_time

    def get_tag(self, obj):
        return obj.kitchen.tag_line

    def get_addresses(self, obj):
        return obj.kitchen.address

    def get_kitchen(self, obj):
        print(obj)
        return obj.kitchen.id

    def get_kitchen_names(self, obj):
        return obj.kitchen.name

    def get_kitchen_images(self, obj):
        if obj.kitchen.image_thumb:
            store_name, kitchen_name = join_string(obj.kitchen.store.name), join_string(obj.kitchen.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
                            'IMAGE_DIR'] + obj.kitchen.image_thumb
        else:
            directory = None

        return directory

    def get_is_open(self, obj):
        if obj.kitchen.status:
            status = time_check(obj.kitchen)
            return status
        else:
            return obj.kitchen.status

    def get_rating(self, obj):

        feedback = KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).aggregate(rating=Avg('rating'))

        if feedback['rating']:
            return ("%.2f" % feedback['rating'])
        else:
            return None

    def get_minimum(self, obj):
        if obj.kitchen.minimum_order:

            int_minimum = int(obj.kitchen.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.kitchen.cost_for_two:
            int_cost = int(obj.kitchen.cost_for_two)
        else:
            int_cost = 0
        return int_cost

    def get_rate(self, obj):
        return KitchenFeedback.objects.filter(kitchen_id=obj.id).count()

    def get_time(self, obj):
        if obj.kitchen.delivery_time:
            int_time = int(obj.kitchen.delivery_time)
        else:
            int_time = 0
        return int_time


class KitchenSearchPriceSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_image')
    is_open = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField('get_rating')
    total_rates = serializers.SerializerMethodField('get_rate')
    minimum_order = serializers.SerializerMethodField('get_minimum')
    cost_for_two = serializers.SerializerMethodField('get_cost')
    delivery_time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Kitchen
        fields = ['id', 'name', 'images', 'ratings', 'total_rates', 'tag_line', 'description', 'location',
                  'address',
                  'is_open', 'minimum_order', 'cost_for_two', 'delivery_time', 'opening_time', 'closing_time']

    def get_time(self, obj):
        if obj.delivery_time:
            int_time = int(obj.delivery_time)
        else:
            int_time = 0
        return int_time

    def get_rate(self, obj):
        return KitchenFeedback.objects.filter(kitchen_id=obj.id, is_deleted=False).count()

    def get_logo(self, obj):
        if obj.logo_thumb:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo_thumb
        else:
            directory = None

        return directory

    def get_image(self, obj):
        if obj.image_thumb:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image_thumb
        else:
            directory = None

        return directory

    def get_rating(self, obj):

        feedback = KitchenFeedback.objects.filter(kitchen_id=obj.id).aggregate(rating=Avg('rating'))

        if feedback['rating']:
            return ("%.2f" % feedback['rating'])
        else:
            return None

    def get_is_open(self, obj):
        if obj.kitchen.status:
            status = time_check(obj.kitchen)
            return status
        else:
            return obj.kitchen.status

    def get_minimum(self, obj):
        if obj.minimum_order:

            int_minimum = int(obj.minimum_order)
        else:
            int_minimum = 0
        return int_minimum

    def get_cost(self, obj):
        if obj.cost_for_two:
            int_cost = int(obj.cost_for_two)
        else:
            int_cost = 0
        return int_cost
