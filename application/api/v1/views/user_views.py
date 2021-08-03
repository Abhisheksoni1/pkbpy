from api.v1.serializers.user_serializer import UserSerializer, UserWalletLogSerializers, CardLogSerializers, \
    CardDetailSerializer
from rest_framework.views import APIView
from apps.users.models import User, Address, UserWalletLog, PaymentModel
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.serializers.user_serializer import UserProfileSerializer, UserWalletSerializer, UserDetailSerializer
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from libraries.Functions import get_token_details
from apps.users.models import User, Address, UserProfile, UserWallet
from rest_framework import status as http_status_codes, permissions
from rest_framework import serializers
import coreapi, coreschema
from rest_framework import schemas
import datetime
from django.db import transaction
from django.utils import timezone
from config import settings
from libraries.Functions import make_dir, image_upload_handler
from libraries.SMS import SendSms
from libraries.Functions import generate_otp
from django.contrib.auth.hashers import make_password
from apps.users.models import User, OtpLog, VerifyOtp
from api.v1.helper import jwt_helper
from django.contrib.auth import authenticate
import base64
from libraries.SMS import SendSms


class UserListViews(APIView):

    def get(self, request):
        try:
            data_user = User.objects.all()
            serializer = UserSerializer(data_user, many=True).data

            response = Response({'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response


class UserProfileEdit(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'name',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter name here'
                )
            ),
            coreapi.Field(
                'dob',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter dob here '
                )
            ),
            # coreapi.Field(
            #     'gender',
            #     required=True,
            #     location='form',
            #     schema=coreschema.String(
            #         description='Enter gender here'
            #     )
            # ),
            coreapi.Field(
                'anniversary',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter anniversary here '
                )
            ),
            # coreapi.Field(
            #     'preference',
            #     required=True,
            #     location='form',
            #     schema=coreschema.String(
            #         description='Enter preference here'
            #     )
            # )
        ]
    )

    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        try:
            """ since mobile number update is optional field so if user not updating mobile then we are not sending otp 
            in response that's why used global variable to keep log of otp
            """
            global v_otp
            v_otp = None
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            user_logged_id = instance['user_id']
            # mobile = request.data.get('mobile')
            name = request.data.get('name')
            dob = request.data.get('dob')
            anniversares = request.data.get('anniversary')
            user = User.objects.get(id=user_logged_id)
            # if mobile:
            #     try:
            #         User.objects.get(mobile=mobile)
            #         return Response({'status': False, 'message': 'This mobile number already exists', },
            #                         status=http_status_codes.HTTP_200_OK)
            #     except Exception as e:
            #         otp = generate_otp(4)
            #         v_otp = otp
            #         try:
            #             log = OtpLog.objects.get(user_id=user_logged_id)
            #             log.otp = otp
            #             log.save()
            #         except Exception:
            #             OtpLog.objects.create(user_id=user_logged_id, otp=otp)
            #         try:
            #             verify = VerifyOtp.objects.get(user_id=user_logged_id)
            #             verify.otp = otp
            #             verify.mobile = mobile
            #             verify.save()
            #         except Exception as e:
            #             VerifyOtp.objects.create(user_id=user_logged_id, otp=otp, mobile=mobile)

            serializer = UserProfileSerializer(User.objects.get(pk=user_logged_id, is_superuser=False),
                                               data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    try:
                        serializer.save()
                        anniversary = serializer.validated_data.get('anniversary', None)
                        preference = serializer.validated_data.get('preference', None)
                        UserProfile.objects.filter(user_id=user_logged_id).update(
                            anniversary=anniversary,
                            updated_on=timezone.now())
                        response = Response(
                            {'status': True, 'message': "Profile has been updated successfully.", 'name': name,
                             'dob': dob, 'anniversary': anniversares, 'mobile': user.mobile},
                            status=http_status_codes.HTTP_202_ACCEPTED)
                        # if v_otp:
                        #     SendSms().send_otp(mobile, v_otp)
                        #     response = Response(
                        #         {'status': True, 'message': "Profile has been updated successfully.", 'otp': v_otp,
                        #          'name': name, 'mobile': user.mobile,
                        #          'dob': dob, 'anniversary': anniversares},
                        #         status=http_status_codes.HTTP_200_OK)

                    except Exception as e:
                        print(e)
                        response = Response({'message': 'Server error.', 'status': False},
                                            status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}

                response = Response({'message': "error ", 'error': tmp_errors, 'status': False},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)
        return response


class UserWalletView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            user_logged_id = instance['user_id']
            user = User.objects.get(id=user_logged_id)
            data_user = UserWallet.objects.get(user_id=user_logged_id, is_deleted=False)
            serializer = UserWalletSerializer(data_user).data

            response = Response({'status': True, 'data': serializer, 'mobile': user.mobile},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class UserDetailView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            user_logged_id = instance['user_id']

            try:
                user = User.objects.get(id=user_logged_id)
                serializer = UserDetailSerializer(user).data
                response = Response({'status': True, 'data': serializer, 'mobile': user.mobile})
            except Exception as e:
                print(e)
                response = Response({'status': False, 'data': []},
                                    status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class UserProfilePic(APIView):
    def post(self, request):
        try:
            profile_pic = request.FILES.get('profile_pic', None)
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            user_logged_id = instance['user_id']
            user = User.objects.get(id=user_logged_id)

            try:
                directory_images = make_dir(
                    settings.MEDIA_ROOT + settings.CUSTOM_DIRS['USER_DIR'] + str(user.id) + '/' + settings.CUSTOM_DIRS[
                        'IMAGE_DIR'])
                img_path = image_upload_handler(request.FILES.get('profile_pic', None),
                                                directory_images)
                user.profile_pic = img_path
                user.save()
                dir = settings.MEDIA_URL + settings.CUSTOM_DIRS['USER_DIR'] + str(user.id) + '/' + \
                      settings.CUSTOM_DIRS[
                          'IMAGE_DIR']
                full_path = dir + img_path
                response = Response(
                    {'status': True, 'message': 'Profile pic updated successfully', 'image_path': full_path,
                     'mobile': user.mobile},
                    status=http_status_codes.HTTP_202_ACCEPTED)
            except Exception as e:
                print(e)
                response = Response({'status': False, 'message': 'image format not supported ', },
                                    status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)
        return response


class UserMobileUpdateVerify(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'mobile',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter mobile here'
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
        ])

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        instance = get_token_details(token)
        user_logged_id = instance['user_id']
        otp = request.data.get('otp', None)
        mobile = request.data.get('mobile', None)
        try:
            verify = VerifyOtp.objects.get(user_id=user_logged_id, otp=otp, mobile=mobile)
            user = request.user
            password = make_password(otp)
            user_detail = {'username': user.username, 'password': otp}
            user.mobile = mobile
            user.otp = otp
            user.password = password
            user.is_active = True
            user.save()
            u1 = authenticate(username=user.username, password=otp)
            token = jwt_helper.get_my_token(user_detail)
            user.auth_token = token['access']
            response = Response({'status': True, 'message': 'Mobile number updated successfully',
                                 'auth_token': token['access'], 'mobile': user.mobile},
                                status=http_status_codes.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            response = Response({'status': False, 'message': 'Entered OTP is not matching', },
                                status=http_status_codes.HTTP_200_OK)
        return response


class WalletListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            user_logged_id = instance['user_id']
            user = User.objects.get(id=user_logged_id)
            try:
                wallet_log = UserWalletLog.objects.filter(user=request.user)
                serializer = UserWalletLogSerializers(wallet_log, many=True).data
                response = Response({'status': True, 'data': serializer, 'mobile': user.mobile},
                                    status=http_status_codes.HTTP_200_OK)
            except Exception as e:
                print(e)
                response = Response({'status': False, 'data': []},
                                    status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class CardLogView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'card_no',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter card_no here'
                )
            ),
            coreapi.Field(
                'date',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter date here'
                )
            ),
            coreapi.Field(
                'card_holder_name',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter year here '
                )
            ),
            coreapi.Field(
                'card_url',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter card_url here'
                )
            ),
            coreapi.Field(
                'card_name',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter card_name here'
                )
            ),
            coreapi.Field(
                'card_type',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter card_type here'
                )
            ),
        ])

    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            user_logged_id = instance['user_id']
            serializer = CardLogSerializers(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save(user_id=user_logged_id)
                    response = Response({'message': 'card details saved successfully', 'status': True},
                                        status=http_status_codes.HTTP_200_OK)
                except Exception as e:
                    print(e)
                    response = Response({'message': 'Server error.', 'status': False},
                                        status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
            else:

                tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
                print(tmp_errors)
                response = Response({'message': "error ", 'error': tmp_errors, 'status': False},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class CardDetails(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            user_logged_id = instance['user_id']
            try:
                payment = PaymentModel.objects.filter(user_id=user_logged_id ,is_deleted = False)
                serializer = CardDetailSerializer(payment, many=True)
                response = Response({'message': 'card details', 'status': True, 'data': serializer.data},
                                    status=http_status_codes.HTTP_200_OK)
            except Exception as e:
                print(e)
                response = Response({'message': 'Card details.', 'status': False, 'data': []},
                                    status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response




class CardDelete(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'card_id',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter card_id here'
                )
            ), ])
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            user_logged_id = instance['user_id']
            card_id = request.data.get('card_id')
            try:
                payment = PaymentModel.objects.get(id=card_id,user_id=user_logged_id,is_deleted=False)
                payment.is_deleted = True
                payment.save()
                response = Response({'message': 'card has been deleted successfully ', 'status': True, },
                                    status=http_status_codes.HTTP_200_OK)
            except Exception as e:
                print(e)
                response = Response({'message': 'card already deleted .', 'status': False, 'data': []},
                                    status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required ", 'status': False},
                         status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response
