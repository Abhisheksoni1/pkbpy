from apps.users.models import User, Address, UserWallet, UserProfile, UserWalletLog, PaymentModel
from rest_framework import serializers
from .address_serializer import AddressSerializer
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
import datetime
from django.utils import timezone
from config import settings


class UserSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField('get_user_address')

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'mobile', 'first_name', 'last_name', 'profile_pic', 'dob', 'gender', 'address'
        ]

    def get_user_address(self, obj):
        get_addresses = Address.objects.filter(user=obj, is_deleted=False)
        get_addresses_ser = AddressSerializer(get_addresses, many=True)
        return get_addresses_ser.data


class UserProfileSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    dob = serializers.DateField(required=False)
    # gender = serializers.CharField(required=True, max_length=20)
    mobile = serializers.IntegerField(required=False)
    # preference = serializers.CharField(required=False, max_length=100)
    anniversary = serializers.DateField(required=False)

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError('Name is required field')
        if len(value) < 3:
            raise serializers.ValidationError('Please Enter at least 3 char ')
        return value

    def validate_dob(self, value):
        if value:
            try:
                dob = datetime.datetime.strptime(str(value), '%Y-%m-%d')
            except Exception as e:
                print(e)
                raise serializers.ValidationError("Incorrect data format, should be YYYY-MM-DD")
        return dob

    # def validate_gender(self, value):
    #     gender_field = ['FEMALE', 'MALE', 'OTHERS']
    #     if value is None:
    #         raise serializers.ValidationError('gender is required field')
    #     if not value in gender_field:
    #         raise serializers.ValidationError('please enter one from MALE,FEMALE,OTHERS')
    #     return value

    def validate_anniversary(self, value):
        if value:
            try:
                ann = datetime.datetime.strptime(str(value), '%Y-%m-%d')
            except Exception as e:
                print(e)
                raise serializers.ValidationError("Incorrect data format, should be YYYY-MM-DD")
        return ann

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dob = validated_data.get('dob', instance.dob)
        # instance.gender = validated_data.get('gender', instance.gender)
        # instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.updated_on = timezone.now()
        instance.save()
        return instance


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ['amount']


class UserDetailSerializer(serializers.ModelSerializer):
    wallet_amount = serializers.SerializerMethodField('get_wallet')
    # preferences = serializers.SerializerMethodField()
    anniversary = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField('get_pic')

    class Meta:
        model = User
        fields = ['name', 'dob', 'mobile', 'wallet_amount', 'anniversary', 'profile_pic']

    def get_wallet(self, obj):
        user = UserWallet.objects.get(user_id=obj.id)
        serializer = UserWalletSerializer(user)
        return serializer.data['amount']

    # def get_preferences(self, obj):
    #     user = UserProfile.objects.get(user_id=obj.id)
    #     serializer = UserProfileDetailserializer(user)
    #     return serializer.data['preferences']

    def get_anniversary(self, obj):
        user = UserProfile.objects.get(user_id=obj.id)
        serializer = UserProfileDetailserializer(user)
        return serializer.data['anniversary']

    def get_pic(self, obj):
        directory = None
        if obj.profile_pic:
            directory = settings.MEDIA_URL + settings.CUSTOM_DIRS['USER_DIR'] +str(obj.id) + '/' + \
                        settings.CUSTOM_DIRS[
                            'IMAGE_DIR'] + obj.profile_pic
        return directory


class UserProfileDetailserializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['preferences', 'anniversary']


class UserProfilePic(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['profile_pic']


class UserWalletLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserWalletLog
        fields = ('amount', 'validity', 'wallet_log_for', 'created_on')


class CardLogSerializers(serializers.Serializer):
    card_no = serializers.CharField(required=True)
    date = serializers.CharField(required=True)
    card_holder_name = serializers.CharField(required=True)
    card_name = serializers.CharField(required=True)
    card_url = serializers.CharField(required=True)
    card_type = serializers.CharField(required=True)

    def create(self, validate_data):
        print(validate_data)
        payment = PaymentModel.objects.create(**validate_data)
        return payment


class CardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = ('id','card_no','date','card_holder_name','card_type','card_name','card_url')
