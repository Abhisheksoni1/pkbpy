from rest_framework.pagination import PageNumberPagination

from apps.stores.models import Kitchen, Store
from rest_framework.response import Response
from api.v1.serializers.store_serializer import StoreKitchenSerializer, StoreDistanceSerializer, \
    StoreDistanceDeliveredSerializer, StoreTakeawaySerializer
from rest_framework.views import APIView
from rest_framework import status as http_status_codes
import coreapi, coreschema
from rest_framework import schemas
from api.v1.helper.jwt_helper import jwt_check
from django.contrib.gis.geos import Point
from rest_framework import serializers
from apps.feedback.models import KitchenFeedback
from itertools import chain
from django.db.models import Avg, Q
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from config import settings
from django.contrib.gis.geos import Point


class StoreListingView(APIView):
    def get(self, request):
        try:
            status = False
            store = Store.objects.filter(is_deleted=False)
            store_serializer = StoreKitchenSerializer(store, many=True).data
            if store_serializer:
                status = True

            response = Response({'status': status, 'data': store_serializer},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response


class StoreDetailView(APIView):

    def get(self, request, pk):

        try:
            store = Store.objects.get(id=pk, is_deleted=False)

            store_serializer = StoreKitchenSerializer(store).data

            response = Response({'status': True, 'data': store_serializer},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response


class StoreDistanceView(APIView):
    schema = schemas.ManualSchema(
        fields=[
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

            coreapi.Field(
                'last_element',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='enter last element count'
                )
            ),

        ])

    def post(self, request):
        try:
            longitude = request.data.get('longitude')
            latitude = request.data.get('latitude')
            pick_up = request.data.get('order_type')
            last_element = int(eval(request.data.get("last_element", "0")))
            # eval was misbehaving So used evel and int both for Safe play
            # print(type(last_element))
            if pick_up not in ['DELIVERY', 'SELF-PICKUP']:
                return Response(
                    {
                        'status': False,
                        'message': 'Pickup_type should be either DELIVERY or SELF-PICKUP '
                    }
                )
            point = Point(float(longitude), float(latitude))
            # store = Store.objects.all()
            # store = [store for store in store if store.location is not None]
            # store_list = [store for store in store if store.location.distance(point) * 100 <= 5]

            # paginator = PageNumberPagination()
            #
            # result_page = paginator.paginate_queryset(store_list, request)
            # print('**',result_page)

            # serializer = StoreDistanceSerializer(store_list, many=True)
            # serializer = paginator.get_paginated_response(serializer.data)

            # result_page1 = paginator.paginate_queryset(store, request)
            # serializer1 = StoreDistanceDeliveredSerializer(store, many=True)
            # serializer1 = paginator.get_paginated_response(serializer1.data)

            # result_page2 = paginator.paginate_queryset(store, request)
            # serializer2 = StoreTakeawaySerializer(store, many=True)
            # serializer2 = paginator.get_paginated_response(serializer2.data)

            if pick_up == 'DELIVERY':
                # with 7 km stores
                # store_list = Store.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                #                  annotate(distance=Distance("location", point)).order_by("distance")
                kitchen = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                    annotate(distance=Distance("location", point)).order_by('location')

                # store = Kitchen.objects.filter(name__icontains=key_word, is_deleted=False)
                stores = [kitchen.store for kitchen in kitchen]
                store_distance = set(stores)
                serializer = StoreDistanceSerializer(store_distance, many=True, context={'point': point})
                #
                # store_list1 = []
                # for store in store_list:
                #     kitchens = Kitchen.objects.filter(store_id=store.id, is_deleted=False)
                #     if kitchens.count != 0:
                #         store_list1.append(store)
                # store_list=[store for store in store_list if store.kitchen.count()!=0]
                # print(store_list)

                # serializer = StoreDistanceSerializer(store_list1, many=True)
                if serializer:
                    response = Response(
                        {'status': True, 'message': 'Within 7 km stores data.',
                         'data': serializer.data},
                        status=http_status_codes.HTTP_200_OK)
                else:
                    store_list1 = Store.objects.all()[last_element:last_element + settings.MAX_STORE_ITEM]
                    store_list = []
                    for store in store_list1:
                        kitchens = Kitchen.objects.filter(store_id=store.id, is_deleted=False)
                        if kitchens.count != 0:
                            store_list.append(store)
                    serializer = StoreDistanceDeliveredSerializer(store_list, many=True)
                    response = Response({'status': True, 'data': serializer.data},
                                        status=http_status_codes.HTTP_200_OK)

            else:
                kitchen = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                    annotate(distance=Distance("location", point)).order_by('location')

                # store = Kitchen.objects.filter(name__icontains=key_word, is_deleted=False)
                stores = [kitchen.store for kitchen in kitchen]
                store_distance = set(stores)
                serializer = StoreTakeawaySerializer(store_distance, many=True,context={'point': point})
                response = Response({'status': True, 'message': 'All store listing ',
                                     'data': serializer.data, },
                                    status=http_status_codes.HTTP_200_OK)
        except IndexError:
            response = Response({'status': True, 'message': 'Data not Available',
                                 'data': [], }, status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class StoreFilterView(APIView):
    schema = schemas.ManualSchema(
        fields=[
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
                'last_element',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='enter last element count'
                )
            ),
            coreapi.Field(
                'order_type',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='enter order_type here'
                )
            ),
            coreapi.Field(
                'Search_key',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter search key field here here.'
                )
            ), ])

    def post(self, request):
        search = request.data.get('Search_key')
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')
        last_element = int(eval(request.data.get("last_element", "0")))
        search_list = ["RATING", "VEG", "HIGH TO LOW", "LOW TO HIGH", "DELIVERY TIME"]
        pick_up = request.data.get('order_type')
        point = Point(float(longitude), float(latitude))
        context = {'point': point}
        if pick_up not in ['DELIVERY', 'SELF-PICKUP']:
            return Response(
                {
                    'status': False,
                    'message': 'Pickup_type should be either DELIVERY or SELF-PICKUP '
                }
            )
        if search not in search_list:
            return Response({'status': False,
                             'message': "Search key should be in RATING, VEG, HIGH TO LOW, LOW TO HIGH, DELIVERY TIME"},
                            status=http_status_codes.HTTP_400_BAD_REQUEST)
        if pick_up == 'DELIVERY':
            if search == 'RATING':
                # suman's code commented

                # kitchen_feedback = KitchenFeedback.objects.values('kitchen').annotate(rating=Avg('rating')).order_by(
                #     '-rating')[last_element:last_element+settings.MAX_STORE_ITEM]

                '''Code Optimize by akhiledra  used Raw query to get fast and accurate result.'''

                # store_list = Kitchen.objects.raw('''SELECT kitchens.id, kitchens.name,
                #                                         CASE WHEN AVG("kitchen_feedbacks"."rating") >=0 THEN  AVG("kitchen_feedbacks"."rating")
                #                                              WHEN AVG("kitchen_feedbacks"."rating") is null THEN 0
                #                                         END AS rating_value
                #                                         FROM "kitchens" left JOIN  kitchen_feedbacks on kitchens.id=kitchen_feedbacks.kitchen_id
                #                                         GROUP BY "kitchens"."id"
                #                                         order by rating_value  asc  limit {} OFFSET {}'''.format(
                #     settings.MAX_STORE_ITEM, last_element))

                # feedback_kitchens = [feedback['kitchen'] for feedback in kitchen_feedback]
                #
                # kitchen_remaining = Kitchen.objects.filter(~Q(id__in=feedback_kitchens))
                #
                # kitchens = Kitchen.objects.filter(id__in=feedback_kitchens)
                #  #all_kitchens = kitchens | kitchen_remaining
                #
                # all_kitchens = chain(kitchens[last_element:last_element+settings.MAX_STORE_ITEM], kitchen_remaining[last_element:last_element+settings.MAX_STORE_ITEM])

                store_list_final = Store.objects.raw('''SELECT stores.id, stores.name,
                                                    CASE WHEN (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                     in (select id from kitchens where store_id= stores.id)) >=0 
                                                        THEN  (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                     in (select id from kitchens where store_id= stores.id))
                                                        WHEN (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                     in (select id from kitchens where store_id= stores.id)) is null THEN 0 
                                                    END AS avg_rate FROM stores
                                                    order by avg_rate desc ''')
                kitchen = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                    annotate(distance=Distance("location", point)).order_by('location')
                stores = [kitchen.store for kitchen in kitchen]
                stores = set(stores)
                store_distance = []
                for store in store_list_final:
                    if store in stores:
                        store_distance.append(store)
                store_distance = store_distance[last_element:last_element + settings.MAX_STORE_ITEM]

                if len(store_distance) > 0:

                    serializer = StoreDistanceSerializer(store_distance, many=True, context=context)
                    response = Response({'status': True, 'message': 'rating based stores', 'data': serializer.data},
                                        status=http_status_codes.HTTP_200_OK
                                        )
                else:
                    store_list = Store.objects.raw('''SELECT stores.id, stores.name,
                                                    CASE WHEN (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                     in (select id from kitchens where store_id= stores.id)) >=0 
                                                        THEN  (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                     in (select id from kitchens where store_id= stores.id))
                                                        WHEN (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                     in (select id from kitchens where store_id= stores.id)) is null THEN 0 
                                                    END AS avg_rate FROM stores
                                                    order by avg_rate desc ''')
                    # print('stores',stores)
                    store_list = store_list[last_element:last_element + settings.MAX_STORE_ITEM]
                    serializer = StoreDistanceDeliveredSerializer(store_list, many=True)
                    response = Response({'status': True, 'message': 'rating based stores', 'data': serializer.data},
                                        status=http_status_codes.HTTP_200_OK
                                        )

            elif search == "HIGH TO LOW":
                store_list_final = Store.objects.filter(is_deleted=False).order_by('-cost_for_two')
                kitchen = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                    annotate(distance=Distance("location", point)).order_by('location')

                stores = [kitchen.store for kitchen in kitchen]
                stores = set(stores)
                store_distance = []
                for store in store_list_final:
                    if store in stores:
                        store_distance.append(store)
                store_distance = store_distance[last_element:last_element + settings.MAX_STORE_ITEM]

                serializer = StoreDistanceSerializer(store_distance, many=True, context=context)

                if serializer.data:
                    response = Response(
                        {'status': True, 'message': 'High to low price based store within 7 km',
                         'data': serializer.data},
                        status=http_status_codes.HTTP_200_OK
                    )
                else:
                    store = Store.objects.filter(is_deleted=False).order_by('-cost_for_two')[
                            last_element:last_element + settings.MAX_STORE_ITEM]
                    serializer = StoreDistanceDeliveredSerializer(store, many=True)
                    response = Response(
                        {'status': True, 'message': 'High to low price based store', 'data': serializer.data},
                        status=http_status_codes.HTTP_200_OK
                    )

            elif search == 'LOW TO HIGH':
                store_list_final = Store.objects.filter(is_deleted=False).order_by('cost_for_two')
                kitchen = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                    annotate(distance=Distance("location", point)).order_by('location')
                store_distance = []
                stores = [kitchen.store for kitchen in kitchen]
                stores = set(stores)

                for store in store_list_final:
                    if store in stores:
                        store_distance.append(store)
                store_distance = store_distance[last_element:last_element + settings.MAX_STORE_ITEM]

                serializer = StoreDistanceSerializer(store_distance, many=True, context=context)
                if serializer.data:
                    response = Response(
                        {'status': True, 'message': 'low to high price  within 7 km based store',
                         'data': serializer.data},
                        status=http_status_codes.HTTP_200_OK)
                else:
                    store = Store.objects.all().order_by('cost_for_two')[
                            last_element:last_element + settings.MAX_STORE_ITEM]
                    serializer = StoreDistanceDeliveredSerializer(store, many=True)
                    response = Response(
                        {'status': True, 'message': 'low to high price based store', 'data': serializer.data},
                        status=http_status_codes.HTTP_200_OK)

            elif search == 'DELIVERY TIME':
                store_list_final = Store.objects.filter(is_deleted=False).order_by('delivery_time')
                kitchen = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                    annotate(distance=Distance("location", point)).order_by('location')
                store_distance = []
                stores = [kitchen.store for kitchen in kitchen]
                # stores = set(stores)
                for store in store_list_final:
                    if store in stores:
                        store_distance.append(store)
                store_distance = store_distance[last_element:last_element + settings.MAX_STORE_ITEM]
                serializer = StoreDistanceSerializer(store_distance, many=True, context=context)

                if serializer.data:
                    response = Response(
                        {'status': True, 'message': 'delivery_time high to low based store', 'data': serializer.data},
                        status=http_status_codes.HTTP_200_OK)
                else:
                    store = Store.objects.filter(is_deleted=False).order_by('delivery_time')[
                            last_element:last_element + settings.MAX_STORE_ITEM]
                    serializer = StoreDistanceDeliveredSerializer(store, many=True)
                    response = Response(
                        {'status': True, 'message': 'low to high price based store', 'data': serializer.data},
                        status=http_status_codes.HTTP_200_OK)
        else:
            if search == 'RATING':

                store_list = Store.objects.raw('''SELECT stores.id, stores.name,
                                                CASE WHEN (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                 in (select id from kitchens where store_id= stores.id)) >=0 
                                                    THEN  (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                 in (select id from kitchens where store_id= stores.id))
                                                    WHEN (select avg(rating) from kitchen_feedbacks where kitchen_id
                                                 in (select id from kitchens where store_id= stores.id)) is null THEN 0 
                                                END AS avg_rate FROM stores
                                                order by avg_rate desc ''')
                store_list = store_list[last_element:last_element + settings.MAX_STORE_ITEM]
                serializer = StoreDistanceSerializer(store_list, many=True)
                response = Response({'status': True, 'message': 'rating based stores', 'data': serializer.data},
                                    status=http_status_codes.HTTP_200_OK
                                    )

            elif search == "HIGH TO LOW":

                store = Store.objects.filter(is_deleted=False).order_by('-cost_for_two')[
                        last_element:last_element + settings.MAX_STORE_ITEM]
                serializer = StoreDistanceSerializer(store, many=True)
                response = Response(
                    {'status': True, 'message': 'High to low price based store', 'data': serializer.data},
                    status=http_status_codes.HTTP_200_OK
                )

            elif search == 'LOW TO HIGH':

                store = Store.objects.all().order_by('cost_for_two')[
                        last_element:last_element + settings.MAX_STORE_ITEM]
                serializer = StoreDistanceSerializer(store, many=True)
                response = Response(
                    {'status': True, 'message': 'low to high price based store', 'data': serializer.data},
                    status=http_status_codes.HTTP_200_OK)

            elif search == 'DELIVERY TIME':

                store = Store.objects.filter(is_deleted=False).order_by('delivery_time')
                serializer = StoreDistanceSerializer(store, many=True)
                response = Response(
                    {'status': True, 'message': 'low to high delivery_time based store', 'data': serializer.data},
                    status=http_status_codes.HTTP_200_OK)

        return response


class StoreSearch(APIView):
    schema = schemas.ManualSchema(
        fields=[
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
            coreapi.Field(
                'key_word',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter order_type here'
                )
            ),
            coreapi.Field(
                'last_element',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='enter last element count'
                )
            ),

        ])

    def post(self, request):
        try:
            longitude = request.data.get('longitude')
            latitude = request.data.get('latitude')
            pick_up = request.data.get('order_type')
            key_word = request.data.get('key_word', None)
            last_element = int(eval(request.data.get("last_element", "0")))
            if pick_up not in ['DELIVERY', 'SELF-PICKUP']:
                return Response(
                    {
                        'status': False,
                        'message': 'order_type should be either DELIVERY or SELF-PICKUP '
                    }
                )
            point = Point(float(longitude), float(latitude))


            # store = Store.objects.filter(name__icontains=key_word, is_deleted=False)[
            #         last_element:last_element + settings.MAX_STORE_ITEM]

            key_word_m = str(key_word).lower()
            store_sql = Store.objects.raw('''SELECT id ,name FROM stores
                                                         WHERE is_deleted=False and lower(name) LIKE '%%{}%%';
                                                        '''.format(key_word_m))[
                    last_element:last_element + settings.MAX_STORE_ITEM]
            # store_list = Store.objects.filter(name__icontains=key_word, is_deleted=False)
            kitchen = Kitchen.objects.filter(is_deleted=False, location__distance_lte=(point, D(m=7000))). \
                annotate(distance=Distance("location", point)).order_by('location')
            store_distance = set()

            stores = [kitchen.store for kitchen in kitchen]
            for store in stores:
                if store in store_sql:
                    store_distance.add(store)

            serializer_delivered = StoreDistanceSerializer(store_distance, many=True, context={'point': point})
            serializer_take = StoreTakeawaySerializer(store_sql, many=True)

            if pick_up == 'DELIVERY':
                if serializer_delivered.data:
                    response = Response(
                        {'status': True, 'message': 'Within 7 km stores data containing keyword.',
                         'data': serializer_delivered.data, },
                        status=http_status_codes.HTTP_200_OK)


                else:
                    response = Response(
                        {'status': False, 'message': 'Within 7 km stores data containing keyword.', 'data': []},
                        status=http_status_codes.HTTP_200_OK)
            else:
                response = Response({'status': True, 'message': 'All store listing ', 'data': serializer_take.data, },
                                    status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
