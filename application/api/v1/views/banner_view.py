from rest_framework.response import Response
from rest_framework.views import APIView
from apps.common.models import PromoBanner
from api.v1.serializers.banner_serializer import BannerSerializer, PromoCodeSerializer, PromoDetailSerializer
from rest_framework import status as http_status_codes
import coreapi, coreschema
from rest_framework import schemas
from apps.discounts.models import PromoCode
from libraries.Functions import get_token_details
from datetime import date, datetime
from pytz import timezone as tz

class BannerView(APIView):
    def get(self, request):

        try:
            status = False
            promo = PromoBanner.objects.filter(status=True, is_deleted=False)
            serializer = BannerSerializer(promo, many=True).data
            if serializer:
                status = True
                # response = Response({ 'status':True,'data': serializer},
                #                     status=http_status_codes.HTTP_200_OK)

            # else:
            response = Response({'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            response = Response({'status': False},
                                status=http_status_codes.HTTP_200_OK)

        return response


class KitchenBannerView(APIView):

    def get(self, request, pk):
        try:
            promo = PromoBanner.objects.filter(status=True, is_deleted=False, kitchen_id=pk)
            serializer = BannerSerializer(promo, many=True).data
            response = Response({'status': True, 'data': serializer, },
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        return response


class PromoCodeView(APIView):
    def get(self, request):
        try:
            promo = PromoCode.objects.filter(status=True, is_deleted=False)
            promo_list = []
            indian_time = tz('Asia/Kolkata')
            for promos in promo:
                if promos.from_date is not None and promos.to_date is not None:
                    now = date.today()
                    time = datetime.now(indian_time).time()
                    if promos.from_date.month <= now.month and promos.to_date.month > now.month:
                        promo_list.append(promos)
                    elif promos.from_date.month == now.month and promos.to_date.month == now.month:
                        if promos.from_date.day <= now.day and promos.to_date.day > now.day:
                            promo_list.append(promos)
                        elif promos.from_date.day <=now.day and promos.to_date.day == now.day:
                            if promos.to_time >= time and promos.from_time<=time :
                                promo_list.append(promos)

            serializer = PromoCodeSerializer(promo_list, many=True).data
            response = Response({'status': True, 'message': "Promo code list", 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'status': False, 'message': 'No Promo code', 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response


class PromoDetailView(APIView):
    def get(self, request, pk):

        try:
            promo = PromoCode.objects.get(id=pk, status=True, is_deleted=False)
            serializer = PromoDetailSerializer(promo).data
            response = Response({'status': True, 'message': "Promo code list", 'data': serializer, },
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'status': False, 'message': 'No Promo code exist of this id ', 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response
