from rest_framework.response import Response
from rest_framework.views import APIView
from apps.stores.models import Item, Kitchen
from api.v1.serializers.item_serializer import ItemSerializer, ItemFeedbackSerializer
from rest_framework import status as http_status_codes
import coreapi, coreschema
from rest_framework import schemas
from libraries.SMS import SendSms
from libraries.Functions import get_token_details
from django.utils import timezone
from apps.feedback.models import ItemFeedback


class ItemDetailView(APIView):

    def get(self, request, pk):
        try:
            item = Item.objects.get(pk=pk,is_deleted = False)
            serializer = ItemSerializer(item).data
            response = Response({'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        return response


class ItemFeedbackView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'feedback_id',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter order_feedback_id here.'
                )
            ),
            coreapi.Field(
                'item_data',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter item data here.'
                )
            ),

        ]
    )

    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            user_detail = get_token_details(token)
            user_logged_id = user_detail['user_id']
            # item_data  = request.data.get('item_data')

            serializer = ItemFeedbackSerializer(data=request.data)

            if serializer.is_valid():
                try:
                    # item_data = eval(serializer.validated_data.pop('item_data'))
                    # print(type(serializer.validated_data.pop('item_data')))

                    data = eval(serializer.validated_data.pop('item_data'))

                    for data_item in data:
                        # print(data_item)
                        ItemFeedback.objects.create(created_by_id=user_logged_id, created_on=timezone.now(), **data_item)
                        # serializer.save(created_by_id=user_logged_id, created_on=timezone.now(),**data_item)
                    response = Response({'message': "Feedback has been submitted successfully.", 'status': True},
                                        status=http_status_codes.HTTP_200_OK)
                except Exception as e:
                    print(e)
                    response = Response({'message': 'Server error', 'status': False},
                                        status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}

                response = Response({'message': "Error ", 'error': tmp_errors, 'status': False},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response = Response({'message': "Login token required.", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response

#
# class CartItemDetail(APIView):
#     schema = schemas.ManualSchema(
#         fields=[
#             coreapi.Field(
#                 'kitchen_id',
#                 required=True,
#                 location='form',
#                 schema=coreschema.String(
#                     description='Enter kitchen_id here.'
#                 )
#             ),
#             coreapi.Field(
#                 'item_id',
#                 required=True,
#                 location='form',
#                 schema=coreschema.String(
#                     description='Enter item_id here.'
#                 )
#             ),
#         ])
#     def post(self,request):
#         try:
#             kitchen_id = request.data.get('kitchen_id')
#             item_id = request.data.get('item_id')
#             kitchen = Kitchen.objects.get(id=kitchen_id)
#
#             item = Item.objects.get(id=item_id,kitchen_id=kitchen_id)
#             serializer = ItemSerializer(item).data
#             response = Response({'status': True, 'data': serializer},
#                                 status=http_status_codes.HTTP_200_OK)
#         except Exception as e:
#             response = Response({'status': False, 'data': []},
#                                 status=http_status_codes.HTTP_200_OK)
#         return response
#
#
