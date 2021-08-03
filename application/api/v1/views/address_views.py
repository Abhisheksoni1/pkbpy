from apps.users.models import Address
from rest_framework.response import Response
from rest_framework.views import APIView
from libraries.Functions import get_token_details
from api.v1.serializers.address_serializer import AddressAddSerializer, AddressUpdateSerializer, AddressSerializer
from apps.users.models import User, Address
from rest_framework import status as http_status_codes, permissions
import coreapi, coreschema
from rest_framework import schemas
from django.utils import timezone


class AddressCreateView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'house_number',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter house number here'
                )
            ),
            coreapi.Field(
                'address_type',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter address type here'
                )
            ),
            coreapi.Field(
                'address_line1',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter address here'
                )
            ),
            coreapi.Field(
                'address_line2',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter address here'
                )
            ),
            coreapi.Field(
                'longitude',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter longitude here'
                )
            ),
            coreapi.Field(
                'latitude',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter latitude here'
                )
            ),
            coreapi.Field(
                'land_mark',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter landmark here'
                )
            ),
            coreapi.Field(
                'state',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter state here'
                )
            ),
            coreapi.Field(
                'country',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter country here'
                )
            ),
            coreapi.Field(
                'pincode',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter pincode here'
                )
            ),
            coreapi.Field(
                'save_as',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter save as here'
                )
            )
        ]
    )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            house_number = request.data.get('house_number', None)
            address_type = request.data.get('address_type', None)
            address_line1 = request.data.get('address_line1', None)
            address_line2 = request.data.get('address_line2', None)
            land_mark = request.data.get('land_mark', None)
            state = request.data.get('state', None)
            country = request.data.get('country', None)
            pincode = request.data.get('pincode', None)
            save_as = request.data.get('save_as', None)
            user = User.objects.get(id=instance['user_id'])
            try:
                Address.objects.get(house_number=house_number, address_type=address_type, address_line1=address_line1,
                                    address_line2=address_line2, land_mark=land_mark, state=state, save_as=save_as,
                                    country=country, pincode=pincode, is_deleted=False)
                return Response({'message': "Address already exists", 'status': False},
                                status=http_status_codes.HTTP_200_OK)
            except Exception as e:
                pass
            serializer = AddressAddSerializer(data=request.data)

            if serializer.is_valid():
                try:
                    serializer.save(user_id=instance['user_id'], created_on=timezone.now())

                    response = Response(
                        {'message': "Address has been created successfully", 'status': True, 'mobile': user.mobile},
                        status=http_status_codes.HTTP_201_CREATED)
                except Exception as e:
                    response = Response({'message': 'Server error.', 'status': False},
                                        status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}

                response = Response({'message': "error ", 'error': tmp_errors, 'status': False},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = Response({'message': "Login Token required", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)
        return response


class AddressUpdateView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'house_number',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter house number here'
                )
            ),
            coreapi.Field(
                'address_id',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter id  here'
                )
            ),

            coreapi.Field(
                'address_type',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter address-type here it should be HOME OR OFFICE OR OTHERS'
                )
            ),
            coreapi.Field(
                'address_line1',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter address here'
                )
            ),
            coreapi.Field(
                'address_line2',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter address here'
                )
            ),
            coreapi.Field(
                'longitude',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter longitude here'
                )
            ),
            coreapi.Field(
                'latitude',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter latitude here'
                )
            ),
            coreapi.Field(
                'land_mark',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter Landmark here'
                )
            ),
            coreapi.Field(
                'state',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter state here'
                )
            ),
            coreapi.Field(
                'country',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter country here'
                )
            ),
            coreapi.Field(
                'pincode',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter pincode here'
                )
            ),
            coreapi.Field(
                'save_as',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter save as here'
                )
            )
        ]
    )

    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            log_user_id = instance['user_id']
            id = request.data['address_id']
            house_number = request.data.get('house_number', None)
            address_type = request.data.get('address_type', None)
            address_line1 = request.data.get('address_line1', None)
            address_line2 = request.data.get('address_line2', None)
            land_mark = request.data.get('land_mark', None)
            state = request.data.get('state', None)
            country = request.data.get('country', None)
            pincode = request.data.get('pincode', None)
            save_as = request.data.get('save_as', None)
            user = User.objects.get(id=log_user_id)
            try:

                Address.objects.get(id=id, house_number=house_number, address_type=address_type,
                                    address_line1=address_line1,
                                    address_line2=address_line2, land_mark=land_mark, state=state, save_as=save_as,
                                    country=country, pincode=pincode)
                return Response({'message': "You have not made any changes", 'status': False},
                                status=http_status_codes.HTTP_200_OK)

            except Exception as e:
                pass
            try:
                address = Address.objects.get(house_number=house_number, address_type=address_type,
                                       address_line1=address_line1,
                                       address_line2=address_line2, land_mark=land_mark, state=state, save_as=save_as,
                                       country=country, pincode=pincode,is_deleted=False)
                print(address)
                return Response({'message': "address already exists", 'status': False},
                                status=http_status_codes.HTTP_200_OK)

            except Exception as e:
                pass

            try:
                address_instance = Address.objects.get(pk=id, user_id=log_user_id, is_deleted=False)
                serializer = AddressUpdateSerializer(address_instance, data=request.data)

                if serializer.is_valid():
                    # Address.objects.filter(pk=id, user_id=log_user_id).update(**serializer.validated_data)
                    try:

                        serializer.save(updated_on=timezone.now(), save_as=save_as)

                        response = Response({'message': "Address has been updated successfully.", 'status': True,
                                             'mobile': user.mobile},
                                            status=http_status_codes.HTTP_202_ACCEPTED)
                    except Exception as e:
                        response = Response({'message': 'Server error.', 'status': False},
                                            status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}

                    response = Response({'message': "error ", 'error': tmp_errors, 'status': False},
                                        status=http_status_codes.HTTP_400_BAD_REQUEST)
            except Exception as e:
                response = Response({'message': "id does not exist", 'status': False},
                                    status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            response = Response({'message': 'un-authorized login', 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class AddressDelete(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'address_id',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter address id here.'
                )
            ),
        ])

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        try:
            id = request.data['address_id']
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            log_user_id = instance['user_id']
            user = User.objects.get(id=log_user_id)
            try:
                Address.objects.get(pk=id, user=log_user_id, is_deleted=False)
                try:
                    Address.objects.filter(pk=id, user=log_user_id).update(is_deleted=True)
                    response = Response(
                        {'message': "Address has been deleted successfully.", 'status': True, 'mobile': user.mobile},
                        status=http_status_codes.HTTP_202_ACCEPTED)
                except Exception as e:
                    response = Response({'message': "Id does not exist.", 'status': False},
                                        status=http_status_codes.HTTP_200_OK)
            except Exception as e:
                response = Response({'message': "This address already deleted", 'status': False},
                                    status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            response = Response({'message': "Login token required.", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)
        return response


class AddressListing(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            instance = get_token_details(token)
            log_user_id = instance['user_id']
            user_id = request.user.id
            user = User.objects.get(id=log_user_id)
            address = Address.objects.filter(user_id=user_id, is_deleted=False).order_by('id')
            serializer = AddressSerializer(address, many=True)
            if serializer:
                response = Response(
                    {'message': 'Address list is', 'status': True, 'data': serializer.data, 'mobile': user.mobile})
            else:
                response = Response({'message': 'No address updated', 'status': False, 'data': []})
        except Exception as e:
            response = Response({'message': "Login token required.", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)
        return response
