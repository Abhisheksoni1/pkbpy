from rest_framework import serializers
from apps.stores.models import Item,  ItemPrice
from apps.orders.models import Order, OrderItems

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id',
                  'order_no',
                  'grand_total',
                  'created_on',
                  'items'

                  ]

    def get_items(self, obj):
        item_qs = obj.orderitems.all()
        serializer = OrderItemsSerializer(item_qs, many=True)
        return serializer.data


class OrderItemsSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItems
        fields = ['item', 'item_name']

    def get_item_name(self, obj):
        return obj.item.name