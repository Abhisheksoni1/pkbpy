from apps.stores.models import Category, Item
from rest_framework import serializers
from .item_serializer import CategoryItemSerializer,ItemSerializer


class KitchenCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_item')

    class Meta:
        model = Category
        fields = ['id','name', 'items']

    def get_item(self, obj):
        items = Item.objects.filter(category_id=obj.id,is_deleted = False)
        serializer = ItemSerializer(items, many=True)
        return serializer.data

