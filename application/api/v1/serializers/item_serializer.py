from apps.stores.models import Item, ItemPrice
from rest_framework import serializers
from apps.orders.models import OrderItems
from apps.taxconfig.models import TaxOnItem, Taxconfig
from rest_framework.response import Response

from apps.discounts.models import DiscountOnItem, Discount
from libraries.Functions import join_string
from config import settings
from apps.feedback.models import ItemFeedback
from django.db.models import Avg
from datetime import date, datetime
from pytz import timezone as tz


class KitchenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'base_price', 'is_outof_stock']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        field = ['id', 'item_id', 'quantity_type', 'unit_price', 'total_price', 'created_on', 'offer_id']


class ItemSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField('get_rating')
    item_price = serializers.SerializerMethodField('get_item_prices')
    # item_taxes = serializers.SerializerMethodField('get_item_tax')
    # item_discounts = serializers.SerializerMethodField('get_item_discount')
    total_discounts = serializers.SerializerMethodField('get_total_discount')
    total_taxes = serializers.SerializerMethodField('get_total_tax')
    image = serializers.SerializerMethodField('get_images')
    base_price = serializers.SerializerMethodField('get_base_prices')

    class Meta:
        model = Item
        fields = ['id', 'name', 'food_type', 'image', 'base_price', 'item_price',
                  'is_variant', 'is_outof_stock', 'total_taxes',
                  'total_discounts', 'ratings']

    def get_base_prices(self, obj):
        int_base = 0
        if obj.base_price:
            int_base = int(obj.base_price)
        return int_base

    def get_rating(self, obj):
        try:
            feedback = ItemFeedback.objects.filter(item_id=obj.id, is_deleted=False).aggregate(rating=Avg('rating'))
            if feedback['rating']:
                return ("%.2f" % feedback['rating'])
        except Exception as e:
            print(e)
            return None

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

    def get_item_prices(self, obj):
        prices = ItemPrice.objects.filter(item_id=obj.id)
        serializer = ItemPriceSerializer(prices, many=True).data
        response = serializer
        if response:

            return response
        else:
            return None

    def get_item_tax(self, obj):
        tax_data = []
        try:
            taxes = TaxOnItem.objects.filter(item_id=obj.id)
            for tax in taxes:
                if tax.tax.is_deleted is False:
                    serializer = ItemTaxSerializer(tax.tax)
                    tax_data.append(serializer.data)
            return tax_data
        except Exception as e:
            print(e)
            return None

    def get_item_discount(self, obj):
        discount_data = []
        discount = DiscountOnItem.objects.filter(item_id=obj.id)
        discount_list = []
        indian_time = tz('Asia/Kolkata')
        for discount in discount:
            if discount.discount.from_date is not None and discount.discount.to_date is not None:
                now = date.today()
                time = datetime.now(indian_time).time()
                if discount.discount.from_date.month <= now.month and discount.discount.to_date.month > now.month:
                    discount_list.append(discount)
                elif discount.discount.from_date.month == now.month and discount.discount.to_date.month == now.month:
                    if discount.discount.from_date.day <= now.day and discount.discount.to_date.day > now.day:
                        discount_list.append(discount)
                    elif discount.discount.from_date.day <= now.day and discount.discount.to_date.day == now.day:
                        if discount.discount.to_time >= time and discount.discount.from_time <= time:
                            discount_list.append(discount)
        for discount in discount_list:
            if discount.discount.is_deleted is False:
                serializer = ItemDiscountSerializer(discount.discount)
                discount_data.append(serializer.data)
        return discount_data

    def get_total_discount(self, obj):
        total_discount = 0.0
        try:
            discount = DiscountOnItem.objects.filter(item_id=obj.id)
            discount_list = []
            indian_time = tz('Asia/Kolkata')
            for discount in discount:
                if discount.discount.from_date is not None and discount.discount.to_date is not None:
                    now = date.today()
                    time = datetime.now(indian_time).time()
                    if discount.discount.from_date.month <= now.month and discount.discount.to_date.month > now.month:
                        discount_list.append(discount)
                    elif discount.discount.from_date.month == now.month and discount.discount.to_date.month == now.month:
                        if discount.discount.from_date.day <= now.day and discount.discount.to_date.day > now.day:
                            discount_list.append(discount)
                        elif discount.discount.from_date.day <= now.day and discount.discount.to_date.day == now.day:
                            if discount.discount.to_time >= time and discount.discount.from_time <= time:
                                discount_list.append(discount)
            for discount in discount_list:
                if discount.discount.is_deleted is False:
                    total_discount = total_discount + float(discount.discount.percentage)
            print(total_discount)
        except Exception as e:
            print(e)
            total_discount = None
        return total_discount

    def get_total_tax(self, obj):
        total_tax = 0.0
        try:
            taxes = TaxOnItem.objects.filter(item_id=obj.id)
            for tax in taxes:
                if tax.tax.is_deleted is False:
                    total_tax = total_tax + float(tax.tax.amount)
            return total_tax
        except Exception as e:
            print(e)
            return None


class ItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPrice
        fields = ['quantity_type', 'price']


class ItemTaxSerializer(serializers.ModelSerializer):
    # amounts = serializers.SerializerMethodField('get_amount')

    class Meta:
        model = Taxconfig
        # fields = '__all__'
        exclude = ['created_on', 'updated_on', 'created_by']


class ItemDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        # fields = '__all__'
        exclude = ['created_on', 'updated_on', 'created_by']


class ItemOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        field = ['name']
        # exclude = ['created_on', 'updated_on', 'created_by']


class ItemFeedbackSerializer(serializers.Serializer):
    feedback_id = serializers.IntegerField(required=True)
    item_data = serializers.CharField(required=True)

    def create(self, validated_data):
        # validated_data = dict(validated_data)
        item = ItemFeedback.objects.create(**validated_data)
        return item

    def validate_rating(self, value):
        if not value:
            raise serializers.ValidationError('rating is required field')
        if int(value) > 5:
            raise serializers.ValidationError('rating should be integer field and less than 5')
        return value

    def validate_order_id(self, value):
        if not value:
            raise serializers.ValidationError('Order-id is required.')

        if value < 0:
            """ safe if someone wants to hack"""
            raise serializers.ValidationError('Order-id should be positive.')
        return value

    def validate_feedback_id(self, value):
        if not value:
            raise serializers.ValidationError('Order-id is required.')
        if value < 0:
            """ safe if someone wants to hack"""
            raise serializers.ValidationError('Order-id should be positive.')
        return value

    # def validate_message:


class CategoryItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_images')
    variant_price = serializers.SerializerMethodField('get_is_varient')
    rating = serializers.SerializerMethodField('get_ratings')
    base_price = serializers.SerializerMethodField('get_base_prices')

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'short_description', 'rating', 'base_price', 'is_outof_stock', 'image',
                  'food_type', 'is_offer_active', 'is_variant', 'variant_price', ]

    def get_is_varient(self, obj):
        if obj.is_variant:
            item_price = ItemPrice.objects.filter(item_id=obj.id)
            serializer = ItemPriceSerializer(item_price, many=True)
            serializer = serializer.data
        else:
            serializer = None

        return serializer

    def get_ratings(self, obj):
        try:
            rating = ItemFeedback.objects.get(item_id=obj.id).rating
            return ("%.2f" % rating)
        except Exception as e:
            return None

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
