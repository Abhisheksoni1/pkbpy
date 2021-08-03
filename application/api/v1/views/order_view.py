import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.forms.models import model_to_dict
from django.utils import timezone

from config import settings
# from libraries.Paytm import Checksum
from apps.common.models import FinancialYear
from apps.feedback.models import OrderFeedback
from apps.discounts.models import PromoCode

from rest_framework.views import APIView
from libraries.Functions import get_token_details
from api.v1.serializers.order_serializer import OrderFeedbackSerializer, OrderPlacedSerializer, OrderListSerializer, \
    OrderItemsDetailSerializer, OrderDetailSerializer, OrderTrackSerializer, OrdertrackStatus
from rest_framework import status as http_status_codes, permissions
from rest_framework.response import Response
from apps.orders.models import OrderItems, Order, OrderLog
from apps.users.models import UserWallet, UserWalletLog
from django.db import transaction
import coreapi, coreschema
from rest_framework import schemas
from django.db.models import Q
from libraries.SMS import SendSms
from libraries.Push_notifications import Register_notification, Order_notification
from apps.feedback.models import KitchenFeedback
from django.db.models import Avg
from apps.users.models import User
from libraries.Paytm import Checksum
import json
import requests


class OrderFeedbackView(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'order_id',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter order-id here.'
                )
            ),
            coreapi.Field(
                'message',
                required=False,
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
        ]
    )

    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            user_detail = get_token_details(token)
            user_logged_id = user_detail['user_id']
            user = User.objects.get(id=user_logged_id)
            try:
                order = Order.objects.get(id=int(request.data['order_id']), user_id=user_logged_id)

                feedback_serializer = OrderFeedbackSerializer(data=request.data)
                if feedback_serializer.is_valid():
                    try:
                        serializer = feedback_serializer
                        serializer.save(order_id=request.data['order_id'], created_by_id=user_logged_id)
                        feedback = OrderFeedback.objects.get(order_id=request.data['order_id'])

                        rating = OrderFeedback.objects.filter(created_by_id=user_logged_id,
                                                              order__kitchen=order.kitchen).aggregate(
                            rating=Avg('rating'))
                        if rating['rating']:
                            avg_rating = float("%.2f" % rating['rating'])
                            try:
                                kitchen = KitchenFeedback.objects.get(created_by_id=user_logged_id,
                                                                      kitchen=order.kitchen)
                                kitchen.rating = avg_rating
                                kitchen.save()
                            except Exception as e:
                                print(e)
                                KitchenFeedback.objects.create(created_by_id=user_logged_id, kitchen=order.kitchen,
                                                               rating=avg_rating)

                        response = Response(
                            {'feedback_id': feedback.id, 'message': "Feedback has been submitted successfully.",
                             'status': True, 'mobile': user.mobile},
                            status=http_status_codes.HTTP_200_OK)
                    except Exception as e:
                        print(e)
                        response = Response({'message': 'feedback already submitted', 'status': False},
                                            status=http_status_codes.HTTP_200_OK)
                else:
                    tmp_errors = {key: feedback_serializer.errors[key][0] for key in feedback_serializer.errors}

                    response = Response({'message': "Error ", 'error': tmp_errors, 'status': False},
                                        status=http_status_codes.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                response = Response({'message': "This order-id is unauthorized.", 'status': False},
                                    status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'message': "Login token required.", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class OrderPlaceView(APIView):
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
                'purchase_method',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter purchase method here and it should be either CASH OR CARD.'
                )
            ),
            coreapi.Field(
                'delivery_type',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter delivery type here and it should be DELIVERY, SELF-PICKUP or DINING.'
                )
            ),
            coreapi.Field(
                'delivery_address',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter delivery address here.'
                )
            ),
            coreapi.Field(
                'promo_code',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter promo code here.'
                )
            ),
            coreapi.Field(
                'wallet_points',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter wallet_points here.'
                )
            ),
            coreapi.Field(
                'total_price',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter total price here.'
                )
            ),
            coreapi.Field(
                'payable_price',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter payable price here.'
                )
            ),
            coreapi.Field(
                'grand_total',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter grand total here.'
                )
            ),
            coreapi.Field(
                'earn_points',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter earn points here.'
                )
            ),
            coreapi.Field(
                'data_item',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data item here.'
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
            coreapi.Field(
                'total_discount',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter total_discount here'
                )
            ),
            coreapi.Field(
                'total_tax',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter total_tax here'
                )
            ),
            coreapi.Field(
                'delivery_charge',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter delivery_charge here.'
                )
            ),
            coreapi.Field(
                'packaging_charges',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter packaging_charges here.'
                )
            ),
            coreapi.Field(
                'special_note',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter special_note here.'
                )
            ),
            coreapi.Field(
                'order_payment_id',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter order_payment_id here.'
                )
            ),
            coreapi.Field(
                'MID',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='Enter MID here.'
                )
            ),

        ]
    )

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            user_logged_id = request.user.id
            user = User.objects.get(id=user_logged_id)
            device_token = request.data.get('device_token')
            delivery_address = request.data.get('delivery_address')
            delivery_charge = request.data.get('delivery_charge')
            packaging_charges = request.data.get('packaging_charges')
            special_note = request.data.get('special_note')
            order_payment_id = request.data.get('order_payment_id')
            mid = request.data.get('MID')
            if not device_token:
                return Response({'message': 'device token is required field.', 'status': False},
                                status=http_status_codes.HTTP_200_OK)

            device_token = request.data.get('device_token')
            promo_code = request.data.get('promo_code', False)

            points = request.data.get('wallet_points', 0.0)
            earn_points = request.data.get('earn_points', 0.0)
            total_discount = request.data.get('total_discount', 0.0)
            total_tax = request.data.get('total_tax', 0.0)
            data = request.data.get('data_item')
            purchase_method= request.data.get('purchase_method')
            try:
                if promo_code:
                    promo_code = PromoCode.objects.get(code__iexact=promo_code, is_deleted=False)
            except Exception as e:
                print(e)
                return Response({'message': 'please enter a valid promo code', 'status': False},
                                status=http_status_codes.HTTP_200_OK)

            try:
                order_serializer = OrderPlacedSerializer(data=request.data)
                if order_serializer.is_valid():
                    try:
                        serializer = order_serializer
                        curr_fin_year = FinancialYear.objects.all()
                        try:
                            last_order = Order.objects.latest(
                                'id')  # Get last Order Detail for Order no. and order_receipt_no
                            last_order_id = last_order.id
                            last_order_no = last_order.order_no
                            last_receipt = last_order.receipt_no
                            order_fin_year = last_order.financial_year
                        except Exception as e:
                            print(e)
                            last_order_id = '0'
                            last_order_no = '0'
                            last_receipt = '0'
                        order_fin_year = FinancialYear.objects.get(id=curr_fin_year[0].id).financial_year

                        if order_fin_year and (order_fin_year == FinancialYear.objects.get(id=curr_fin_year[
                            0].id).financial_year):  # Restart Receipt_no from 1 if Financial Year change.
                            receipt_no = eval(last_receipt) + 1
                        else:
                            receipt_no = 1

                        if type(data) is str:
                            data = eval(data)
                        else:
                            data = eval(str(data))

                        with transaction.atomic():
                            order = serializer.save(user_id=user_logged_id, order_no=eval(last_order_no) + 1,
                                                    financial_year=order_fin_year, receipt_no=receipt_no,
                                                    points=points, delivery_address=delivery_address,
                                                    offer_id=promo_code.id if promo_code else None,
                                                    discount_by_id=request.user.id,
                                                    earn_points=earn_points,
                                                    created_on=timezone.now(),
                                                    delivery_charge=float(delivery_charge),
                                                    packaging_charges=float(packaging_charges),
                                                    total_discount=total_discount, special_note=special_note,
                                                    order_payment_id=order_payment_id)

                            order_log = OrderLog.objects.create(
                                order_id=order.id,
                                order_status='0',
                                created_on=timezone.now(),
                            )

                            user_wallet = UserWallet.objects.get(user_id=user_logged_id)
                            amount = float(user_wallet.amount)
                            new_amount = amount - float(points)
                            user_wallet.amount = new_amount
                            user_wallet.save()
                            UserWalletLog.objects.create(user_id=user_logged_id, amount=-float(points),
                                                         created_on=timezone.now())

                            for data_item in data:
                                OrderItems.objects.create(order_id=order.id, **data_item)



                        response = Response(
                            {'message': "Order has been placed successfully", 'order_number': eval(last_order_no) + 1,
                             'order_id': order.id, 'user_id': user_logged_id, 'mobile': user.mobile, 'status': True},
                            status=http_status_codes.HTTP_201_CREATED)
                        if mid and order_payment_id and purchase_method != 'CASH':
                            paytmParams = dict()
                            checksum = Checksum.generate_checksum(paytmParams, settings.MERCHANT_SECRET)
                            paytmParams["CHECKSUMHASH"] = checksum
                            paytmParams["MID"] = mid
                            paytmParams["ORDERID"] = order_payment_id
                            post_data = json.dumps(paytmParams)
                            url = "https://securegw.paytm.in/order/status"
                            res = requests.post(url, data=post_data,
                                                headers={"Content-type": "application/json"}).json()
                            if res['STATUS']=="TXN_SUCCESS":
                                layer = get_channel_layer()
                                # kitchen = Kitchen.objects.get(id=data.get('kitchen'))
                                # print(kitchen.group_name)
                                async_to_sync(layer.group_send)('kitchen', {
                                    "type": "kitchen.message",
                                    "kitchen_id": order.kitchen.id,
                                    "username": request.user.username,
                                    "message": "{}".format(model_to_dict(order)),
                                })
                                SendSms().pkb_order_before_confirmation(number=request.user.mobile)
                                order_push = Order_notification(device_token, eval(last_order_no) + 1)
                            else:
                                user_wallet.amount = user_wallet.amount + float(points)
                                user_wallet.save()
                                UserWalletLog.objects.create(user_id=user_logged_id, amount=+float(points),
                                                             created_on=timezone.now())
                                SendSms().pkb_order_canceled(number=user.mobile, order_id=order.order_no)
                                order.order_status = 3
                                order.save()
                                OrderLog.objects.create(
                                    order_id=order.id,
                                    order_status='3',
                                    created_on=timezone.now(),
                                )

                        if purchase_method == 'CASH':
                            layer = get_channel_layer()
                            # kitchen = Kitchen.objects.get(id=data.get('kitchen'))
                            # print(kitchen.group_name)
                            async_to_sync(layer.group_send)('kitchen', {
                                "type": "kitchen.message",
                                "kitchen_id": order.kitchen.id,
                                "username": request.user.username,
                                "message": "{}".format(model_to_dict(order)),
                            })
                            SendSms().pkb_order_before_confirmation(number=request.user.mobile)
                            order_push = Order_notification(device_token, eval(last_order_no) + 1)

                    except Exception as e:
                        print(e)
                        response = Response({'message': 'Server error.', 'status': False},
                                            status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    tmp_errors = {key: order_serializer.errors[key][0] for key in order_serializer.errors}
                    print(tmp_errors)
                    response = Response({'message': "error ", 'error': tmp_errors, 'status': False},
                                        status=http_status_codes.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print(e)
                response = Response({'message': "Invalid Token", 'status': False},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            response = Response({'message': "Login Token required", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class OrderListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user_logged_id = request.user.id
            user = User.objects.get(id=user_logged_id)
            try:
                orders = Order.objects.filter(user_id=user_logged_id).order_by('-created_on')

                serializer = OrderListSerializer(orders, many=True).data
                response = Response({'status': True, 'data': serializer, 'mobile': user.mobile},
                                    status=http_status_codes.HTTP_200_OK)

            except Exception as e:
                print(e)
                response = Response({'status': False, 'data': []},
                                    status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': "Login token required.", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class OrderDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            user_logged_id = request.user.id
            user = User.objects.get(id=user_logged_id)
            try:
                order = Order.objects.get(id=pk, user_id=user_logged_id)

                try:

                    serializer = OrderDetailSerializer(order).data
                    response = Response({'status': True, 'data': serializer, 'mobile': user.mobile},
                                        status=http_status_codes.HTTP_200_OK)

                except Exception as e:
                    print(e)
                    response = Response({'status': False, 'data': []},
                                        status=http_status_codes.HTTP_200_OK)
            except Exception as e:
                print(e)
                response = Response({'message': "Order id is un-authorized", 'status': False},
                                    status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            response = Response({'message': "Login token required.", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class OrderTrack(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            user_logged_id = request.user.id
            user = User.objects.get(id=user_logged_id)
            try:
                order = Order.objects.get(id=pk, user_id=user_logged_id)

                try:
                    # order = OrderLog.objects.filter(order_id=pk)
                    serializer = OrderTrackSerializer(order).data
                    response = Response({'status': True, 'data': serializer, 'mobile': user.mobile},
                                        status=http_status_codes.HTTP_200_OK)

                except Exception as e:
                    print(e)
                    response = Response({'status': False, 'data': []},
                                        status=http_status_codes.HTTP_200_OK)
            except Exception as e:
                response = Response({'message': "Order id is un-authorized", 'status': False},
                                    status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            response = Response({'message': "Login token required.", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response


class OrderTrackStatusBasis(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user_logged_id = request.user.id
            user = User.objects.get(id=user_logged_id)
            orders_delivered = []
            orders = []
            order = Order.objects.filter(~Q(order_status=3), user_id=user_logged_id).order_by('-created_on')
            for order in order:
                if order.order_status == 2:
                    orders_delivered.append(order)
                else:
                    orders.append(order)
            print(orders_delivered)
            order_feedback = []
            for order in orders_delivered:
                try:
                    OrderFeedback.objects.get(order_id=order.id)
                except Exception as e:
                    order_feedback.append(order)

            # order_feedback = OrderFeedback.objects.filter(order_id__in=orders_delivered)
            order_remain = order_feedback
            if len(order_feedback) > 2:
                order_remain = order_feedback[:2]

            try:
                # order = OrderLog.objects.filter(order_id=pk)
                if len(orders) > 3:
                    orders = orders[:3]
                serializer = OrdertrackStatus(orders, many=True).data
                serializer_remain = OrdertrackStatus(order_remain, many=True).data
                response = Response({'status': True, 'order_data': serializer, 'feedback_order': serializer_remain,
                                     'mobile': user.mobile},
                                    status=http_status_codes.HTTP_200_OK)

            except Exception as e:
                print(e)
                response = Response({'status': False, 'data': []},
                                    status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'message': "Login token required.", 'status': False},
                                status=http_status_codes.HTTP_401_UNAUTHORIZED)

        return response
