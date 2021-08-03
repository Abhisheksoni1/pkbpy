from apps.stores.models import Store, Kitchen,Category, Item , ItemPrice, KitchenAttribute, StoreAttribute
from apps.taxconfig.models import Taxconfig,TaxOnItem
from apps.discounts.models import Discount,DiscountOnItem
from rest_framework import serializers
from datetime import date, datetime
from pytz import timezone as tz




class ItemDetailSerializer(serializers.ModelSerializer):
    item_prices = serializers.SerializerMethodField()
    tax_on_item = serializers.SerializerMethodField()
    discount_on_item = serializers.SerializerMethodField()
    total_tax = serializers.SerializerMethodField()
    total_discount = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'description',
            'short_description',
            'category',
            'image',
            'food_type',
            'is_offer_active',
            'is_variant',
            'base_price',
            'is_outof_stock',
            'status',
            'is_deleted',
            'created_on',
            'updated_on',
            'item_prices',
            'tax_on_item',
            'discount_on_item',
            'total_tax',
            'total_discount'
        ]

    def get_item_prices(self, obj):
        if obj.is_variant:
            prices = obj.itemprices.all()
            price_ser = ItemPriceSerializer(prices, many=True)
            return price_ser.data
        else:
            return None

    def get_total_tax(self, obj):
        total_tax = TaxOnItem.objects.filter(item=obj,tax__is_deleted=False)
        tot = 0.0
        for tax_item in total_tax:
            tot = tot + float(tax_item.tax.amount)

        return tot

    def get_total_discount(self, obj):
        total_discount = 0.0
        discount_list=[]
        indian_time = tz('Asia/Kolkata')

        try:
            discounts = DiscountOnItem.objects.filter(item=obj,is_deleted=False)
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
            total_discount = 0.0  # if any Exception occurs, 0 discount % will be apply.

        return total_discount



        return total


    def get_tax_on_item(self, obj):
        tax_item_data = []
        try:
            taxes = TaxOnItem.objects.filter(item=obj)
            for tax_item in taxes:
                tax_serializer = TaxSerializer(tax_item.tax)
                tax_item_data.append(tax_serializer.data)
            return tax_item_data

        except Exception as e:
            print(e)
            return None

    def get_discount_on_item(self, obj):
        discount_item_data = []
        indian_time = tz('Asia/Kolkata')
        try:
            discounts = DiscountOnItem.objects.filter(item=obj)

            for discount in discounts:
                if discount.discount.from_date is not None and discount.discount.to_date is not None:
                    now = date.today()
                    time = datetime.now(indian_time).time()
                    if discount.discount.from_date.month <= now.month and discount.discount.to_date.month > now.month:
                        discount_serializer = DiscountSerializer(discount.discount)
                        discount_item_data.append(discount_serializer.data)
                    elif discount.discount.from_date.month == now.month and discount.discount.to_date.month == now.month:
                        if discount.discount.from_date.day <= now.day and discount.discount.to_date.day > now.day:
                            discount_serializer = DiscountSerializer(discount.discount)
                            discount_item_data.append(discount_serializer.data)
                        elif discount.discount.from_date.day <= now.day and discount.discount.to_date.day == now.day:
                            if discount.discount.to_time >= time:
                                discount_serializer = DiscountSerializer(discount.discount)
                                discount_item_data.append(discount_serializer.data)

            # for discount in discounts:
            #     discount_serializer = DiscountSerializer(discount.discount)
            #     discount_item_data.append(discount_serializer.data)

            return discount_item_data
        except Exception as e:
            print(e)
            return None


class ItemPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemPrice
        fields = '__all__'

class TaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Taxconfig
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = '__all__'

