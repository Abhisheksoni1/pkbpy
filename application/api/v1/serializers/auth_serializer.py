from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from libraries.Functions import generate_otp
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from libraries.SMS import SendSms


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        is_active = 1 if user.is_active == True else 0

        token['mobile'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_active'] = is_active
        return token


class GetUserSerializer(serializers.Serializer):
    mobile = serializers.IntegerField(required=True)

    def validate_mobile(self, value):
        """
        Validates mobile number
        :param value:
        :return: mobile as value if no exception raised
        """

        if not value:
            raise serializers.ValidationError('mobile is required field.')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(mobile=value).exists():
                    if len(str(value)) != 10:
                        raise serializers.ValidationError('mobile numer should be of 10 digits')
                    return value
                else:
                    raise serializers.ValidationError('mobile number is already registered.')


            except Exception as error:
                raise error

    def create(self, validated_data):
        """
        Register new user with validated_data
        :param validated_data:
        :return: Newly created user object
        """
        otp = generate_otp(4)
        # SendSms().send_otp(validated_data['mobile'], otp)
        try:
            validated_data['mobile'] = validated_data['mobile']
            validated_data['password'] = make_password(otp)
            validated_data['is_staff'] = False
            validated_data['is_superuser'] = False
            validated_data['is_mobile_verified'] = False
            validated_data['login_otp'] = otp
            user = get_user_model().objects.create(**validated_data)


        except Exception as e:
            raise e
        return user
