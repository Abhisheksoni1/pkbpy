from rest_framework import serializers
from apps.stores.models import Store, Kitchen, Category, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', ]


class CategorySerializer(serializers.ModelSerializer):
    item_names = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'item_names', ]

    def get_item_names(self, obj):
        qs = obj.items.filter(category_id=obj.id)
        return ItemSerializer(qs, many=True).data


class KitchenSerializer(serializers.ModelSerializer):
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = Kitchen
        fields = ['id', 'name', 'category_names', ]

    def get_category_names(self, obj):
        qs = obj.categories.filter(kitchen_id=obj.id)
        return CategorySerializer(qs, many=True).data


class StoreSerializer(serializers.ModelSerializer):
    kitchen_names = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'name', 'kitchen_names']

    def get_kitchen_names(self, obj):
        qs = obj.kitchens.filter(store_id=obj.id)
        return KitchenSerializer(qs, many=True).data
