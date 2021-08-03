from apps.stores.models import Kitchen, Store
from apps.feedback.models import KitchenFeedback
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.serializers.kitchen_serializer import KitchenDetailSerializer, KitchenFeedbackSerializer, \
    KitchenSearchSerializer, ItemSearchSerializer, KitchenCategoryCountSerializer, KitchenSearchratingSerializer, \
    KitchenSearchPriceSerializer, kitchenStatusSerial
from rest_framework import status as http_status_codes, permissions
import coreapi, coreschema
from rest_framework import schemas
from config import settings
from rest_framework import generics
from apps.stores.models import Item
from django.db.models import Avg
from django.db.models import Q
from itertools import chain
from apps.stores.models import Category, Item
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from config import settings
from django.contrib.gis.geos import Point


class KitchenDetailView(APIView):

    def get(self, request, pk):

        try:
            kitchen = Kitchen.objects.get(id=pk, is_deleted=False)

            serializer = KitchenDetailSerializer(kitchen).data

            response = Response({'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response


class KitchenFeedbackView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'kitchen_id',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter kitchen-id here.'
                )
            ),
            coreapi.Field(
                'message',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter message here.'
                )
            ),

            coreapi.Field(
                'rating',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter rating here.'
                )
            ),
        ])

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            user_logged_id = request.user.id
            feedback_serializer = KitchenFeedbackSerializer(data=request.data)
            if feedback_serializer.is_valid():
                try:
                    serializer = feedback_serializer
                    serializer.save(created_by_id=user_logged_id)

                    response = Response({'message': " Feedback has been submitted successfully.", 'status': True},
                                        status=http_status_codes.HTTP_201_CREATED)

                except Exception as e:
                    response = Response({'message': 'Server error.', 'status': False},
                                        status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                tmp_errors = {key: feedback_serializer.errors[key][0] for key in feedback_serializer.errors}
                print(tmp_errors)

                response = Response({'message': "error", 'errors': tmp_errors, 'status': False},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = Response({'message': "Login token required", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class KitchenSearchView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'key_word',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter key_word here.'
                )
            ),
            coreapi.Field(
                'last_element',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter last_element here.'
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
                'order_type',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter order_type here'
                )
            ),
        ])

    def post(self, request, ):
        key_word = request.data.get('key_word')
        last_element = int(request.data.get('last_element', 0))
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')
        order_type = request.data.get('order_type')
        t = key_word.replace(" ", '')
        if len(t) <= 0:
            return Response(
                {
                    'status': False,
                    'message': 'length without space should be grater than 1'
                }
            )
        if order_type not in ['DELIVERY', 'SELF-PICKUP']:
            return Response(
                {
                    'status': False,
                    'message': 'Pickup_type should be either DELIVERY or SELF-PICKUP '
                }
            )
        point = Point(float(longitude), float(latitude))
        try:
            key_word_m = str(key_word).lower()
            kitchen = Kitchen.objects.raw('''SELECT id ,name FROM kitchens
                                            WHERE is_deleted=False and lower(name) LIKE '%%{}%%';
                                            '''.format(key_word_m))[last_element:last_element + settings.MAX_STORE_ITEM]
            # kitchen = Kitchen.objects.filter(name__icontains=key_word,is_deleted=False)[last_element:last_element + settings.MAX_STORE_ITEM]
            item = Item.objects.raw('''SELECT id ,name FROM items
                                        WHERE is_deleted=False and lower(name) LIKE '%%{}%%';
                                        '''.format(key_word_m))[last_element:last_element + settings.MAX_STORE_ITEM]

            if order_type == 'DELIVERY':
                kitchen_delivery = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                    annotate(distance=Distance("location", point)).order_by('location')
                kitchens = []
                for kitchen_d in kitchen_delivery:
                    if kitchen_d in kitchen:
                        kitchens.append(kitchen_d)
                items = []
                for item_d in item:
                    if item_d.category.kitchen in kitchen_delivery:
                        items.append(item_d)

                item = ItemSearchSerializer(items, many=True).data

                kitchen = KitchenSearchSerializer(kitchens, many=True).data
                data = {'kitchen': kitchen, 'item': item}
                if kitchen and item:
                    response = Response({'status': True, 'data': data},
                                        status=http_status_codes.HTTP_200_OK)
                elif item:
                    response = Response({'status': True, 'data': {'item': item}},
                                        status=http_status_codes.HTTP_200_OK)
                elif kitchen:
                    response = Response({'status': True, 'data': {'kitchen': kitchen}},
                                        status=http_status_codes.HTTP_200_OK
                                        )
                else:
                    response = Response({'status': False, 'data': {}},
                                        status=http_status_codes.HTTP_200_OK)
            else:
                kitchen_delivery = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=20000))). \
                    annotate(distance=Distance("location", point)).order_by('location')
                kitchens = []
                for kitchen_d in kitchen_delivery:
                    if kitchen_d in kitchen:
                        kitchens.append(kitchen_d)
                items = []
                for item_d in item:
                    if item_d.category.kitchen in kitchen_delivery:
                        items.append(item_d)

                item = ItemSearchSerializer(items, many=True).data

                kitchen = KitchenSearchSerializer(kitchens, many=True).data
                data = {'kitchen': kitchen, 'item': item}
                if kitchen and item:
                    response = Response({'status': True, 'data': data},
                                        status=http_status_codes.HTTP_200_OK)
                elif item:
                    response = Response({'status': True, 'data': {'item': item}},
                                        status=http_status_codes.HTTP_200_OK)
                elif kitchen:
                    response = Response({'status': True, 'data': {'kitchen': kitchen}},
                                        status=http_status_codes.HTTP_200_OK
                                        )
                else:
                    response = Response({'status': False, 'data': {}},
                                        status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': {}},
                                status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class kitchenStatusView(APIView):
    def get(self, request, pk):
        try:
            kitchen = Kitchen.objects.get(id=pk, is_deleted=False)

            serializer = kitchenStatusSerial(kitchen).data

            response = Response({'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response


class KitchenDetailCatView(APIView):
    def get(self, request, pk):

        try:
            kitchen = Kitchen.objects.get(id=pk, is_deleted=False)

            serializer = KitchenCategoryCountSerializer(kitchen).data

            response = Response({'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response

# class FilterView(APIView):
#     schema = schemas.ManualSchema(
#         fields=[
#             coreapi.Field(
#                 'Search_key',
#                 required=True,
#                 location='form',
#                 schema=coreschema.String(
#                     description='Enter search key field here here.'
#                 )
#             ), ])
#
#     def post(self, request):
#         search = request.data.get('Search_key')
#         search_list = ["RATING", "VEG", "HIGH TO LOW", "LOW TO HIGH", "DELIVERY TIME"]
#         if search not in search_list:
#             return Response({'status': False,
#                              'message': "Search key should be in RATING, VEG, HIGH TO LOW, LOW TO HIGH, DELIVERY TIME"},
#                             status=http_status_codes.HTTP_400_BAD_REQUEST)
#         if search == 'RATING':
#             kitchen_feedback = KitchenFeedback.objects.values('kitchen').annotate(rating=Avg('rating')).order_by(
#                 '-rating')
#
#             feedback_kitchens = [feedback['kitchen'] for feedback in kitchen_feedback]
#
#             kitchen_remaining = Kitchen.objects.filter(~Q(id__in=feedback_kitchens))
#
#             kitchens = Kitchen.objects.filter(id__in=feedback_kitchens)
#             # all_kitchens = kitchens | kitchen_remaining
#
#             all_kitchens = chain(kitchens, kitchen_remaining)
#
#             serializer = KitchenSearchPriceSerializer(all_kitchens, many=True)
#             response = Response({'status': True, 'message': 'rating based Kitchens', 'data': serializer.data},
#                                 status=http_status_codes.HTTP_200_OK
#                                 )
#         # if search=='VEG':
#         #     category = Category.objects.filter
#
#         if search == "HIGH TO LOW":
#             kitchen = Kitchen.objects.order_by('-cost_for_two')
#             serializer = KitchenSearchPriceSerializer(kitchen, many=True)
#             response = Response(
#                 {'status': True, 'message': 'High to low price based Kitchens', 'data': serializer.data},
#                 status=http_status_codes.HTTP_200_OK
#             )
#         if search == 'LOW TO HIGH':
#             kitchen = Kitchen.objects.order_by('cost_for_two')
#             serializer = KitchenSearchPriceSerializer(kitchen, many=True)
#             response = Response(
#                 {'status': True, 'message': 'low to high price based Kitchens', 'data': serializer.data},
#                 status=http_status_codes.HTTP_200_OK)
#         if search == 'DELIVERY TIME':
#             kitchen = Kitchen.objects.order_by('delivery_time')
#             serializer = KitchenSearchPriceSerializer(kitchen, many=True)
#             response = Response(
#                 {'status': True, 'message': 'delivery_time high to low based Kitchens', 'data': serializer.data},
#                 status=http_status_codes.HTTP_200_OK)
#         return response
#
#
#
#
#
