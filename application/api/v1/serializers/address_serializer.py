from apps.users.models import Address, User
from rest_framework import serializers
from django.utils import timezone

# from .user_serializer import UserSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'house_number', 'address_type', 'address_line1', 'address_line2', 'land_mark',
                  'latitude', 'longitude', 'state', 'pincode', 'country', 'save_as']
        # fields = '__all__'


class AddressAddSerializer(serializers.ModelSerializer):
    house_number = serializers.CharField(max_length=32, required=True)
    address_type = serializers.CharField(max_length=200, required=True)
    address_line1 = serializers.CharField(max_length=200, required=True)
    address_line2 = serializers.CharField(max_length=200, required=False)
    land_mark = serializers.CharField(max_length=64, required=False)
    state = serializers.CharField(max_length=200, required=True)
    country = serializers.CharField(max_length=200, required=True)
    pincode = serializers.CharField(max_length=100, required=True)
    latitude = serializers.CharField(max_length=100, required=True)
    longitude = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Address
        fields = ['house_number', 'address_type', 'address_line1', 'address_line2', 'land_mark', 'state', 'country',
                  'pincode', 'latitude', 'longitude', 'save_as']

    def create(self, validated_data):
        # print(validated_data)
        address = Address.objects.create(**validated_data)
        return address

    def validate_house_number(self, value):
        if not value:
            raise serializers.ValidationError('house number is required')
        # if len(value) > 32:
        #     raise serializers.ValidationError('house number length should be less than 32')
        return value

    def validate_address_type(self, value):
        address_type = ['HOME', 'OFFICE', 'OTHERS']
        if not value:
            raise serializers.ValidationError('address type is required')

        if not value in address_type:
            raise serializers.ValidationError('address type  should be HOME or OFFICE or OTHERS')
        return value

    def validate_address_line1(self, value):
        if not value:
            raise serializers.ValidationError('address line 1 is required')

        if len(value) < 2:
            raise serializers.ValidationError('address should have more then 2 char')
        return value

    def validate_address_line2(self, value):
        if not value:
            raise serializers.ValidationError('address line 2 is required')

        if len(value) < 2:
            raise serializers.ValidationError('address should be more then 2 char')
        return value

    def validate_state(self, value):
        if not value:
            raise serializers.ValidationError('state is required field ')

        if len(value) < 2:
            raise serializers.ValidationError('state should have more then 2 char')

        return value

    def validate_country(self, value):
        if not value:
            raise serializers.ValidationError('country is required field ')

        if len(value) < 2:
            raise serializers.ValidationError('country should have more then 2 char')

        return value

    def validate_pincode(self, value):
        if not value:
            raise serializers.ValidationError('pincode is required field ')

        if len(value) < 2:
            raise serializers.ValidationError('pincode should have more then 2 integer')

        return value


class AddressUpdateSerializer(serializers.ModelSerializer):
    house_number = serializers.CharField(max_length=32, required=True)
    address_id = serializers.IntegerField(required=True)
    address_type = serializers.CharField(max_length=200, required=True)
    address_line1 = serializers.CharField(max_length=200, required=True)
    address_line2 = serializers.CharField(max_length=200, required=True)
    land_mark = serializers.CharField(max_length=64, required=False)
    state = serializers.CharField(max_length=200, required=True)
    country = serializers.CharField(max_length=200, required=True)
    pincode = serializers.CharField(max_length=100, required=True)
    latitude = serializers.CharField(max_length=100, required=True)
    longitude = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Address
        fields = ['house_number', 'address_id', 'address_type', 'address_line1', 'address_line2', 'land_mark',
                  'latitude', 'longitude', 'state', 'country', 'pincode']

    def update(self, instance, validated_data):
        instance.house_number = validated_data.get('house_number', instance.house_number)
        instance.address_type = validated_data.get('address_type', instance.address_type)
        instance.address_line1 = validated_data.get('address_line1', instance.address_line1)
        instance.address_line2 = validated_data.get('address_line2', instance.address_line2)
        instance.land_mark = validated_data.get('land_mark', instance.land_mark)

        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.save_as = validated_data.get('save_as',instance.save_as)
        instance.save()
        # instance.objects.update(**validated_data)
        return instance

    def validate_house_number(self, value):
        if not value:
            raise serializers.ValidationError('house number is required')
        # if len(value) > 32:
        #     raise serializers.ValidationError('house number length should be less than 32')
        return value

    def validate_address_id(self, value):
        if not value:
            raise serializers.ValidationError('Address id is required.')
        if value < 0:
            """ safe if someone wants to hack"""
            raise serializers.ValidationError('Address id should be positive integer.')
        return value

    def validate_address_type(self, value):
        address_type = ['HOME', 'OFFICE', 'OTHERS']
        if not value:
            raise serializers.ValidationError('Address type is required.')

        if not value in address_type:
            raise serializers.ValidationError('Address type should be HOME or OFFICE or OTHERS.')
        return value

    def validate_address_line1(self, value):
        if not value:
            raise serializers.ValidationError('Address line 1 is required.')

        if len(value) < 2:
            raise serializers.ValidationError('Address should have more then 2 char.')
        return value

    def validate_address_line2(self, value):
        if not value:
            raise serializers.ValidationError('Address line 2 is required.')

        if len(value) < 2:
            raise serializers.ValidationError('Address should be more then 2 char.')
        return value

    def validate_state(self, value):
        if not value:
            raise serializers.ValidationError('State is required field.')

        if len(value) < 2:
            raise serializers.ValidationError('State should have more then 2 char.')

        return value

    def validate_country(self, value):
        if not value:
            raise serializers.ValidationError('Country is required field.')

        if len(value) < 2:
            raise serializers.ValidationError('Country should have more then 2 char.')

        return value

    def validate_pincode(self, value):
        if not value:
            raise serializers.ValidationError('Pin-code is required field.')

        if len(value) < 2:
            raise serializers.ValidationError('Pin-code should have more then 2 integer.')

        return value


class AddressDeleteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    fields = ['id']
