from apps.orders.models import Order
from apps.users.models import User, Address, UserWallet
from rest_framework import serializers
from .address_serializer import AddressSerializer
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField('get_user_address')
    wallet_point = serializers.SerializerMethodField()
    has_previous_order = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'mobile', 'first_name', 'last_name', 'profile_pic', 'dob', 'gender', 'address',
            'wallet_point', 'name', 'has_previous_order'
        ]

    def get_has_previous_order(self, obj):
        get_previous_order = Order.objects.filter(user=obj).exists()
        return get_previous_order

    def get_user_address(self, obj):
        get_addresses = Address.objects.filter(user=obj, is_deleted=False)
        get_addresses_ser = AddressSerializer(get_addresses, many=True)
        return get_addresses_ser.data

    def get_wallet_point(self, obj):
        try:
            userwallet = obj.userwallet.amount
        except:
            userwallet = 0.00

        return userwallet


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=100)
    dob = serializers.DateField(required=False)
    gender = serializers.CharField(required=True, max_length=20)
    email = serializers.EmailField(required=True, max_length=100)

    class Meta:
        model = User
        fields = ['name', 'dob', 'gender', 'email']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.dob = validated_data.get('dob')
        instance.gender = validated_data.get('gender')
        instance.email = validated_data.get('email')
        return instance
