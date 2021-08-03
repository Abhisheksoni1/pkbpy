from apps.users.models import Address, User
from rest_framework import serializers


# from .user_serializer import UserSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_type', 'address_line1', 'address_line2', 'address_line1', 'state', 'pincode',
                  'deliver_to', 'country']
        # fields = '__all__'


class AddressAddSerializer(serializers.ModelSerializer):
    address_type = serializers.CharField(max_length=200, required=True)
    address_line1 = serializers.CharField(max_length=200, required=True)
    address_line2 = serializers.CharField(max_length=200, required=True)
    state = serializers.CharField(max_length=200, required=True)
    country = serializers.CharField(max_length=200, required=True)
    pincode = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Address
        fields = ['id', 'address_type', 'address_line1', 'address_line2', 'state', 'country', 'pincode']

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)
        return address


class AddressUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    address_type = serializers.CharField(max_length=200, required=True)
    address_line1 = serializers.CharField(max_length=200, required=True)
    address_line2 = serializers.CharField(max_length=200, required=True)
    state = serializers.CharField(max_length=200, required=True)
    country = serializers.CharField(max_length=200, required=True)
    pincode = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Address
        fields = ['id', 'address_type', 'address_line1', 'address_line2', 'state', 'country', 'pincode']

    def update(self, instance, validated_data):
        instance.address_type = validated_data.get('address_type')
        instance.address_line1 = validated_data.get('address_line1')
        instance.address_line2 = validated_data.get('address_line2')
        instance.state = validated_data.get('state')
        instance.country = validated_data.get('country')
        instance.pincode = validated_data.get('pincode')
        # instance.objects.update(**validated_data)
        return instance


class AddressDeleteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    fields = ['id']
