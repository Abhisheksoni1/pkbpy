from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework import status as http_status_codes
from api.v1.serializers.auth_serializer import GetUserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate

from apps.stores.models import StoreManager
from apps.users.models import LoginLog
from django.utils import timezone
from api.v1.helper import jwt_helper
from apps.users.models import User, OtpLog
from libraries.SMS import SendSms
from libraries.Functions import generate_otp
from django.contrib.auth.hashers import make_password
import coreapi, coreschema
from rest_framework import schemas
from libraries.Push_notifications import Register_notification
from libraries.Functions import get_token_details
import uuid


class GetUserApiView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'mobile',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter mobile number here'
                )
            ),
            coreapi.Field(
                'name',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter name here'
                )
            ),

        ]
    )

    def post(self, request):
        mobile = request.data.get('mobile', None)
        name = request.data.get('name', None)
        name_val = name.strip(" ")
        if len(name_val) < 2:
            return Response({'message': 'name should contain more than 2 char ', 'status': False},
                            status=http_status_codes.HTTP_200_OK)
        try:
            user = User.objects.get(mobile=mobile)
            response = {}
            if user:
                otp = generate_otp(4)
                try:

                    log = OtpLog.objects.get(user=user)
                    log.otp = otp
                    log.save()

                except Exception:
                    OtpLog.objects.create(user=user, otp=otp)

                user.name = name
                user.login_otp = otp
                if "Manager" not in user.group_name:
                    user.password = make_password(otp)
                user.save()
                SendSms().send_otp(mobile, otp)

                response = Response({'message': "OTP has been sent to your mobile", 'otp': otp, 'status': True},
                                    status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            serializer = GetUserSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    user = serializer.save(username=str(uuid.uuid1().hex))
                    user.name = name
                    user.save()
                    otp = generate_otp(4)
                    OtpLog.objects.create(user=user, otp=otp)
                    group = Group.objects.get(name__exact="User")
                    group.user_set.add(user)
                    group.save()
                    response = Response(
                        {'message': "OTP has been sent to your mobile. Please verify.",
                         'status': True},
                        status=http_status_codes.HTTP_201_CREATED)
                except Exception as e:
                    print(e)
                    response = Response({'message': 'Server error.', 'status': False},
                                        status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
                response = Response({'message': "errors", 'error': tmp_errors, 'status': False},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)

        return response


class LoginApiView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'mobile',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter Mobile number here'
                )
            ),
            coreapi.Field(
                'otp',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter otp here'
                )
            ),

            coreapi.Field(
                'device_token',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter device_token here'
                )
            ),

        ]
    )

    def post(self, request):
        username = request.data.get('mobile', None)
        password = request.data.get('otp', None)

        device_token = request.data.get('device_token', None)
        try:
            otp_log = OtpLog.objects.get(user__mobile=username)
            if username and password:
                user = User.objects.get(mobile=username)
                username = user.username
                try:
                    if "Manager" in user.group_name:
                        password = StoreManager.objects.get(manager=user).manager_p
                    user = authenticate(username=username, password=password)  # mobile as username and otp as password
                    if user and user.is_active:
                        user_detail = {'username': user.username, 'password': password}

                        token = jwt_helper.get_my_token(user_detail)
                        user.last_login = timezone.now()
                        user.save()
                        auth_user_log = LoginLog()
                        auth_user_log.login_time = timezone.now()
                        auth_user_log.device_token = device_token
                        auth_user_log.auth_token = token['access']
                        auth_user_log.is_loggedin = True
                        auth_user_log.user = user
                        auth_user_log.save()

                        Register_notification(device_token)
                        otp_log.delete()

                        return Response({'message': 'You have been successfully logged in',
                                         'data': jwt_helper.get_my_token(user_detail),
                                         'status': True},
                                        status=http_status_codes.HTTP_200_OK)
                    else:
                        return Response({'message': 'Invalid OTP.', 'status': False},
                                        status=http_status_codes.HTTP_200_OK)
                except Exception as e:
                    print(e)
                    return Response({'message': 'Server error.', 'status': False},
                                    status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'message': 'mobile and otp are required fields', 'status': False},
                                status=http_status_codes.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message': 'Otp expired.', 'status': False},
                            status=http_status_codes.HTTP_200_OK)


class LogoutApiView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'device_token',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter device_token here'
                )
            ), ])

    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            device_token = request.data.get('device_token')
            instance = get_token_details(token)
            user_logged_id = instance['user_id']
            login = LoginLog.objects.get(user_id=user_logged_id, device_token=device_token, status=True)
            login.status = 0
            login.save()
            response = Response({'message': "Log-out successfully", 'status': True},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response
