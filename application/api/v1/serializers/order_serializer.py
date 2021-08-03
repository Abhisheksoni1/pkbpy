from rest_framework import serializers
from apps.feedback.models import OrderFeedback
from apps.orders.models import OrderItems, Order, OrderLog
from .item_serializer import OrderItemSerializer, ItemOrderDetailSerializer, ItemDiscountSerializer, \
    ItemPriceSerializer, ItemTaxSerializer
from apps.stores.models import Item, ItemPrice
from libraries.Functions import join_string
from config import settings
from django.db.models import Sum, Avg
from apps.feedback.models import KitchenFeedback
from decimal import Decimal
from apps.users.models import User
from apps.discounts.models import DiscountOnItem
from django.utils import timezone
from apps.taxconfig.models import TaxOnItem, Taxconfig
from rest_framework.response import Response
from datetime import date, datetime
from pytz import timezone as tz
from apps.discounts.models import DiscountOnItem, Discount
from libraries.Functions import join_string
from config import settings
from apps.feedback.models import ItemFeedback


class OrderFeedbackSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(required=True)
    message = serializers.CharField(required=False, max_length=1000)
    rating = serializers.IntegerField(required=True)

    # rating = serializers.IntegerField(required=True,max_value=5)

    class Meta:
        model = OrderFeedback
        fields = ['message', 'order_id', 'rating']

    def create(self, validated_data):
        order = OrderFeedback.objects.create(**validated_data)
        return order

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

    # def validate_message:
    def validate_message(self, value):
        if not value:
            raise serializers.ValidationError('Message method is required')
        if len(value) < 3:
            raise serializers.ValidationError('At least 3 char is required')

        return value


class OrderPlacedSerializer(serializers.Serializer):
    kitchen_id = serializers.IntegerField(required=True)
    purchase_method = serializers.CharField(required=False)
    delivery_type = serializers.CharField(required=True)
    delivery_address = serializers.CharField(required=True)
    # wallet_points = serializers.IntegerField(required=False)
    total_price = serializers.DecimalField(required=True, max_digits=7, decimal_places=2)
    payable_price = serializers.DecimalField(required=True, max_digits=7, decimal_places=2)
    grand_total = serializers.DecimalField(required=True, max_digits=7, decimal_places=2)
    # data_item = serializers.CharField(required=True)
    total_discount = serializers.DecimalField(required=False, max_digits=7, decimal_places=2)
    total_tax = serializers.DecimalField(required=True, max_digits=7, decimal_places=2)

    def create(self, validated_data):
        validated_data = dict(validated_data)
        orders = Order.objects.create(**validated_data)
        return orders

    def validate_kitchen_id(self, value):
        if not value:
            raise serializers.ValidationError('Kitchen id is required.')
        if value < 0:
            """ safe if someone wants to hack"""
            raise serializers.ValidationError('Kitchen id should be positive.')
        return value

    def validate_delivery_address(self, value):
        if not value:
            raise serializers.ValidationError('delivery_address is required.')

    # def validate_purchase_method(self, value):
    #     purchase_method = ['CASH', 'CARD']
    #     if not value:
    #         raise serializers.ValidationError('Purchase method is required.')
    #
    #     if not value in purchase_method:
    #         raise serializers.ValidationError('Purchase method should be either CASH OR CARD.')
    #     return value

    def validate_delivery_type(self, value):
        delivery_type = ['DELIVERY', 'SELF-PICKUP', 'DINING']
        if not value:
            raise serializers.ValidationError('Delivery type is required.')

        if not value in delivery_type:
            raise serializers.ValidationError('Delivery type should be DELIVERY, SELF-PICKUP,DINING.')
        return value

    def validate_total_price(self, value):
        if value < 0:
            value = 0
        return value

    def validate_payable_price(self, value):
        if value < 0:
            value = 0
        return value

    def validate_grand_total(self, value):
        if value < 0:
            value = 0
        return value


class OrderListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_item_names')
    rating = serializers.SerializerMethodField('get_ratings')
    kitchen_name = serializers.SerializerMethodField('get_kitchen')
    kitchen_address = serializers.SerializerMethodField('get_address')
    kitchen_image = serializers.SerializerMethodField('get_kitchen_images')
    order_status = serializers.SerializerMethodField('get_order_stat')
    kitchen_rating = serializers.SerializerMethodField('get_kitchen_ratings')
    kitchen_total_rate = serializers.SerializerMethodField('get_kitchen_total')
    kitchen_id = serializers.SerializerMethodField('get_kitchen_ids')
    # kitchen_delivery_charge = serializers.SerializerMethodField('get_kitchen_delivery')
    kitchen_minimum_order = serializers.SerializerMethodField('kitchen_minimum')
    kitchen_location = serializers.SerializerMethodField('kitchen_locations')

    # packaging_charges = serializers.SerializerMethodField('get_charges')

    class Meta:
        model = Order
        fields = ['id', 'order_no', 'updated_on', 'kitchen_id', 'kitchen_name', 'kitchen_address', 'kitchen_image',
                  'payable_price', 'kitchen_rating', 'kitchen_total_rate', 'delivery_charge', 'created_on',
                  'kitchen_minimum_order', 'kitchen_location', 'delivery_type', 'packaging_charges',
                  'delivery_address', 'items', 'rating', 'order_status']

    def get_charges(self, obj):
        return obj.kitchen.packing_charges

    def kitchen_locations(self, obj):
        # print(obj.kitchen.location)
        return str(obj.kitchen.location)

    def get_kitchen_ratings(self, obj):
        feedback = KitchenFeedback.objects.filter(kitchen_id=obj.kitchen.id, is_deleted=False).aggregate(
            rating=Avg('rating'))

        if feedback['rating']:
            return ("%.2f" % feedback['rating'])
        else:
            return None

    def get_kitchen_ids(self, obj):
        return obj.kitchen.id

    def kitchen_minimum(self, obj):
        return obj.kitchen.minimum_order

    def get_kitchen_total(self, obj):
        return KitchenFeedback.objects.filter(kitchen_id=obj.kitchen.id, is_deleted=False).count()

    def get_kitchen_delivery(self, obj):
        return obj.kitchen.delivery_charges

    def get_order_stat(self, obj):
        return OrderLog.objects.filter(order_id=obj.id).latest('created_on').order_status

    def get_kitchen(self, obj):
        return obj.kitchen.name

    def get_address(self, obj):
        return obj.kitchen.address

    def get_item_names(self, obj):
        order_item = OrderItems.objects.filter(order_id=obj.id)
        serial = OrderItemsDetailSerializer(order_item, many=True)
        return serial.data

    def get_ratings(self, obj):
        try:
            status = False
            feedback = OrderFeedback.objects.get(order_id=obj.id)
            rating = feedback.rating
            message = feedback.message
            if rating:
                status = True
        except Exception as e:
            status = False
            rating = None
            message = None

        return {'status': status, 'rating': rating, }

    def get_kitchen_images(self, obj):

        if obj.kitchen.image:
            store_name, kitchen_name = join_string(obj.kitchen.store.name), join_string(obj.kitchen.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.kitchen.image
        else:
            directory = None

        return directory


class OrderItemsDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField('get_item_names')
    food_type = serializers.SerializerMethodField('get_food')
    is_variant = serializers.SerializerMethodField('get_variant')
    item_image = serializers.SerializerMethodField('get_images')
    id = serializers.SerializerMethodField('item_id')
    item_price = serializers.SerializerMethodField('get_item_prices')
    item_taxes = serializers.SerializerMethodField('get_item_tax')
    item_discounts = serializers.SerializerMethodField('get_item_discount')

    class Meta:
        model = OrderItems
        fields = ['id', 'item_name', 'quantity_type', 'quantity', 'unit_price', 'tax_value', 'total_price', 'food_type',
                  'is_variant', 'item_image', 'item_price', 'item_taxes', 'item_discounts']

    def item_id(self, obj):
        return obj.item.id

    def get_item_prices(self, obj):

        if obj.quantity_type=='Normal':
            price = obj.item.base_price
        else:
            try:
                prices = ItemPrice.objects.get(item_id=obj.item.id, quantity_type=obj.quantity_type)
                price = prices.price
            except:
                price=0.0
        return price

    def get_item_tax(self, obj):
        total_tax = 0.0
        try:
            taxes = TaxOnItem.objects.filter(item_id=obj.item.id)
            for tax in taxes:
                if tax.tax.is_deleted is False:
                    total_tax = total_tax + float(tax.tax.amount)
            return total_tax
        except Exception as e:
            print(e)
            return None

    def get_item_discount(self, obj):
        total_discount = 0.0
        try:
            discounts = DiscountOnItem.objects.filter(item_id=obj.item.id)
            discount_list = []
            indian_time = tz('Asia/Kolkata')
            for discount in discounts:
                if discount.discount.from_date is not None and discount.discount.to_date is not None:
                    now = date.today()
                    time = datetime.now(indian_time).time()
                    if discount.discount.from_date.month <= now.month and discount.discount.to_date.month > now.month:
                        discount_list.append(discount)
                    elif discount.discount.from_date.month == now.month and discount.discount.to_date.month == now.month:
                        if discount.discount.from_date.day <= now.day and discount.discount.to_date.day > now.day:
                            discount_list.append(discount)
                        elif discount.discount.from_date.day <= now.day and discount.discount.to_date.day == now.day:
                            if discount.discount.to_time >= time:
                                discount_list.append(discount)
            for discount in discount_list:
                    total_discount = total_discount + float(discount.discount.percentage)

        except Exception as e:
            print(e)
            total_discount = None
        return total_discount

    def get_images(self, obj):
        if obj.item.image:
            store_name, kitchen_name, category_name, item_name = join_string(obj.item.category.kitchen.store.name), \
                                                                 join_string(
                                                                     obj.item.category.kitchen.name), join_string(
                obj.item.category.name), join_string(obj.item.name)

            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
                            'CATEGORY_DIR'] + category_name + '/' + \
                        settings.CUSTOM_DIRS['ITEM_DIR'] + item_name + '/' + settings.CUSTOM_DIRS[
                            'IMAGE_DIR'] + obj.item.image
        else:
            directory = None
        return directory

    def get_item_names(self, obj):
        return obj.item.name

    def get_food(self, obj):
        return obj.item.food_type

    def get_variant(self, obj):
        return obj.item.is_variant


class OrderDetailSerializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField('get_order_items')
    mobile_no = serializers.SerializerMethodField('get_mobile')
    # total_tax = serializers.SerializerMethodField('get_taxes')
    total_price = serializers.SerializerMethodField('get_price')
    message = serializers.SerializerMethodField('get_messages')
    kitchen_name = serializers.SerializerMethodField('get_kitchens')
    kitchen_image = serializers.SerializerMethodField('get_kitchen_images')
    kitchen_address = serializers.SerializerMethodField('get_address')
    kitchen_location = serializers.SerializerMethodField('get_location')
    kitchen_mobile = serializers.SerializerMethodField('get_kitchen_m')
    rating = serializers.SerializerMethodField('get_ratings')
    # delivery_charge = serializers.SerializerMethodField('get_charge')
    # packaging_charges = serializers.SerializerMethodField('get_packing')
    payable_price = serializers.SerializerMethodField('get_payable')
    kitchen_id = serializers.SerializerMethodField('get_kitchen_ids')
    wallet_points = serializers.SerializerMethodField('get_wallet_point')
    status = serializers.SerializerMethodField('get_stat')
    delivery_time = serializers.SerializerMethodField('get_delivery')

    # total_discount = serializers.SerializerMethodField('get_total_discounts')

    class Meta:
        model = Order
        fields = ['id', 'order_item', 'message', 'order_no', 'purchase_method', 'delivery_charge', 'packaging_charges',
                  'total_price', 'total_tax', 'rating', 'kitchen_id', 'delivery_type', 'wallet_points',
                  'total_discount', 'kitchen_location', 'status', 'delivery_time',
                  'payable_price', 'mobile_no', 'created_on',
                  'delivery_address', 'kitchen_name', 'kitchen_image', 'kitchen_address', 'kitchen_mobile',
                  ]

    # def get_total_discounts(self, obj):
    #     orders = OrderItems.objects.filter(order_id=obj.id)
    #     total_discount = 0.0
    #     try:
    #         for order in orders:
    #             discount = DiscountOnItem.objects.filter(item_id=order.item.id)
    #             for discount in discount:
    #                 if discount.discount.is_deleted is False:
    #                     total_discount = total_discount + float(discount.discount.amount)
    #     except Exception as e:
    #         print(e)
    #         total_discount = None
    #     return total_discount
    def get_location(self, obj):
        return str(obj.kitchen.location)

    def get_wallet_point(self, obj):
        return obj.points

    def get_kitchen_ids(self, obj):
        return obj.kitchen.id

    def get_packing(self, obj):
        if obj.kitchen.packing_charges:
            return ("%.2f" % obj.kitchen.packing_charges)
        else:
            return 0.0

    def get_charge(self, obj):
        if obj.kitchen.delivery_charges:
            return ("%.2f" % obj.kitchen.delivery_charges)
        else:
            return 0.0

    def get_payable(self, obj):
        if obj.payable_price:
            return ("%.2f" % obj.payable_price)
        else:
            return 0.0

    def get_stat(self, obj):
        k = OrderLog.objects.filter(order_id=obj.id).latest('created_on').order_status
        return k

    def get_delivery(self, obj):
        try:
            log = OrderLog.objects.get(order_id=obj.id, order_status=2)
            time = log.created_on
        except Exception as e:
            print(e)
            time = None
        return time

    def get_messages(self, obj):
        k = OrderLog.objects.filter(order_id=obj.id).latest('created_on').order_status
        if k == 0:
            message = 'The order with {} is pending for confirmation'.format(obj.kitchen.name)
        if k == 1:
            message = 'The order with {} is confirmed'.format(obj.kitchen.name)
        if k == 2 and obj.delivery_type == "DELIVERY":
            message = 'The order with {} was delivered'.format(obj.kitchen.name)

        if k == 2 and obj.delivery_type == "SELF-PICKUP":
            message = 'The order with {} was Picked-up'.format(obj.kitchen.name)
        if k == 3:
            message = 'The order with {} is declined'.format(obj.kitchen.name)
        if k == 4 and obj.delivery_type == "DELIVERY":
            message = 'The order with {} is dispatched'.format(obj.kitchen.name)
        if k == 4 and obj.delivery_type == "SELF-PICKUP":
            message = 'The order with {} is packed'.format(obj.kitchen.name)
        return message

    def get_kitchen_m(self, obj):
        return obj.kitchen.mobile

    def get_ratings(self, obj):
        try:
            status = False
            feedback = OrderFeedback.objects.get(order_id=obj.id)
            rating = feedback.rating
            if rating:
                status = True
        except Exception as e:
            status = False
            rating = None

        return {'status': status, 'rating': rating}

    def get_order_items(self, obj):
        orders = OrderItems.objects.filter(order_id=obj.id)
        serializer = OrderItemsDetailSerializer(orders, many=True)
        return serializer.data

    def get_mobile(self, obj):
        user_no = obj.user.mobile
        return user_no

    #
    # def get_taxes(self, obj):
    #     tax = OrderItems.objects.filter(order_id=obj.id).aggregate(Sum('tax_value'))
    #     if tax['tax_value__sum']:
    #         return ("%.2f" % tax['tax_value__sum'])
    #     else:
    #         return 0.0

    def get_price(self, obj):
        tax = OrderItems.objects.filter(order_id=obj.id).aggregate(Sum('total_price'))
        if tax['total_price__sum']:
            return ("%.2f" % tax['total_price__sum'])
        else:
            return 0.0

    def get_kitchens(self, obj):
        return obj.kitchen.name

    def get_kitchen_images(self, obj):

        if obj.kitchen.image:
            store_name, kitchen_name = join_string(obj.kitchen.store.name), join_string(obj.kitchen.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.kitchen.image
        else:
            directory = None

        return directory

    def get_address(self, obj):
        return obj.kitchen.address


class OrderTrackSerial(serializers.ModelSerializer):
    class Meta:
        model = OrderLog
        fields = ['order_status', 'created_on']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'mobile']


class OrderTrackSerializer(serializers.ModelSerializer):
    order_log = serializers.SerializerMethodField('get_order')
    delivery_boy = serializers.SerializerMethodField('get_delivery')
    current_delivery_time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Order
        fields = ['id', 'current_delivery_time', 'estimated_delivery_time', 'delivery_boy', 'order_log',
                  'delivery_type', 'created_on']

    def get_time(self, obj):
        try:
            order = OrderLog.objects.get(order_id=obj.id, order_status=1)
            time = order.created_on
            current_time = timezone.now()
            time_remains = current_time - time
            time_sec = int(time_remains.total_seconds())
            time_min = int(time_sec / 60)

            if (int(obj.estimated_delivery_time) - time_min) > 0:
                return str(int(obj.estimated_delivery_time) - time_min)
            else:
                return str(0)
        except Exception as e:
            print(e)
            return str(obj.estimated_delivery_time)

    def get_order(self, obj):
        order_log = OrderLog.objects.filter(order_id=obj.id).latest('created_on')
        serializer = OrderTrackSerial(order_log).data
        return serializer

    def get_delivery(self, obj):
        serial = None
        if obj.delivery_boy:
            user = User.objects.get(id=int(obj.delivery_boy))
            serial = DeliverySerializer(user).data
        return serial


class OrdertrackStatus(serializers.ModelSerializer):
    kitchen_name = serializers.SerializerMethodField('get_kitchens')
    kitchen_image = serializers.SerializerMethodField('get_kitchen_images')
    items_data = serializers.SerializerMethodField('get_item_data')

    class Meta:
        model = Order
        fields = ['id', 'order_status', 'kitchen_name', 'kitchen_image', 'items_data', 'delivery_type']

    def get_kitchens(self, obj):
        return obj.kitchen.name

    def get_kitchen_images(self, obj):

        if obj.kitchen.image:
            store_name, kitchen_name = join_string(obj.kitchen.store.name), join_string(obj.kitchen.name)
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS[
                            'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.kitchen.image
        else:
            directory = None

        return directory

    def get_item_data(self, obj):
        items = OrderItems.objects.filter(order_id=obj.id)
        serializer = OrderStatusTrackSerializer(items, many=True)
        return serializer.data


class OrderStatusTrackSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = OrderItems
        fields = ['item_id', 'item_name']

    def get_name(self, obj):
        return obj.item.name
