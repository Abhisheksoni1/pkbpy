import coreapi
import coreschema
import requests
from datetime import datetime

from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import schemas
from rest_framework.views import APIView
from rest_framework import status as http_status_codes, permissions
from libraries.Paytm import Checksum
from django.conf import settings
from apps.payment.models import PaymentHistory
import json


class GenerateChecksum(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'MID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter MERCHANT ID.'
                )
            ),
            coreapi.Field(
                'ORDER_ID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Order ID'
                )
            ),

            coreapi.Field(
                'TXN_AMOUNT',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Total order value'
                )
            ),

            coreapi.Field(
                'CUST_ID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='CUST ID'
                )
            ),

            coreapi.Field(
                'CHANNEL_ID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='CHANNEL_ID'
                )
            ),

            coreapi.Field(
                'WEBSITE',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='WEBSITE'
                )
            ),

            coreapi.Field(
                'INDUSTRY_TYPE_ID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='INDUSTRY_TYPE_ID'
                )
            ),

            coreapi.Field(
                'CALLBACK_URL',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='CALLBACK_URL For verify Checksum'
                )
            ),

            coreapi.Field(
                'MOBILE_NO',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='ENTER USER MOBILE'
                )
            ),

            coreapi.Field(
                'EMAIL',
                required=False,
                location='form',
                schema=coreschema.String(
                    description='ENTER USER EMAIL'
                )
            ),
            #
            # coreapi.Field(
            #     'MERC_UNQ_REF',
            #     required=True,
            #     location='form',
            #     schema=coreschema.String(
            #         description='ENTER USER MERC_UNQ_REF'
            #     )
            # ),

        ])

    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # print(request.data)
        mid = request.POST.get('MID')
        order_id = request.POST.get('ORDER_ID')
        order_total = request.POST.get('TXN_AMOUNT')
        import json
        # user_logged_id = request.user.id
        print(request.POST)
        # print(order_id)

        # print(mid)
        param_dict = {
            'MID': mid,
            'ORDER_ID': str(order_id),
            'TXN_AMOUNT': str(order_total),
            'CUST_ID': request.POST.get("CUST_ID"),
            'INDUSTRY_TYPE_ID': request.POST.get("INDUSTRY_TYPE_ID"),
            'WEBSITE': request.POST.get("WEBSITE"),
            'CHANNEL_ID': request.POST.get("CHANNEL_ID"),
            "CALLBACK_URL": request.POST.get("CALLBACK_URL")
        }
        if request.POST.get("MOBILE_NO"):
            param_dict['MOBILE_NO'] = request.POST.get("MOBILE_NO")
        if request.POST.get("EMAIL"):
            param_dict["EMAIL"] = request.POST.get("EMAIL")
        print(param_dict)
        checksum = Checksum.generate_checksum(param_dict, settings.MERCHANT_SECRET)
        # print(checksum)
        response = {
            "CHECKSUMHASH": checksum,
            "ORDER_ID": order_id,
            "payt_STATUS": "1"
        }

        # response = Response({'message': " checksum genreted.", 'status': True, 'param_data': param_dict},
        #                     status=http_status_codes.HTTP_202_ACCEPTED)
        return Response(response)


class VerifyChecksum(APIView):
    """
    {
        'ORDERID': 'pkb66UbAl',
        'MID': 'JikZMu08131000071064',
        'TXNID': '20190902111212800110168513885783684',
        'TXNAMOUNT': '1.00',
        'PAYMENTMODE': 'CC',
        'CURRENCY': 'INR',
        'TXNDATE': '2019-09-02 17:26:38.0',
        'STATUS': 'TXN_SUCCESS',
        'RESPCODE': '01',
        'RESPMSG': 'Txn Success',
        'GATEWAYNAME': 'HDFC',
        'BANKTXNID': '201924587289783',
        'BANKNAME': 'HDFC',
        'CHECKSUMHASH': '1sYCwVE+8v7roeAmeGS3w3NFefDC3H7XHQUr9826lNmTNyphX2lTC4Sq1WUsGqMm3Yk0IgtBMuV7ZPuAaD4UISJPCBBSQB
                    oNMloCFGPBJAU='
    }
    """
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'ORDERID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'MID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'TXNID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'TXNAMOUNT',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'PAYMENTMODE',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'CURRENCY',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'TXNDATE',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'STATUS',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'RESPCODE',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'RESPMSG',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'GATEWAYNAME',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'BANKTXNID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'BANKNAME',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            ),
            coreapi.Field(
                'CHECKSUMHASH',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter data.'
                )
            )

        ])

    # permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        # print(request.data)
        print()
        return HttpResponse(request.GET.get("errorMessage"))

    def post(self, request):
        checksum_data = request.data
        print(checksum_data)
        html = "<script type='text/javascript'>function closeWindow(){setTimeout(function(){window.close();},3000);};window.onload = closeWindow()</script>"
        try:
            checksum_data = checksum_data
            print(checksum_data)
            print(checksum_data.keys())
            response_dict = {}
            for i in checksum_data.keys():
                response_dict[i] = checksum_data[i]
                if i == 'CHECKSUMHASH':
                    checksum = checksum_data[i]

            verify = Checksum.verify_checksum(response_dict, settings.MERCHANT_SECRET, checksum)
            # print(response_dict)

            if verify:
                if response_dict['STATUS'] == 'TXN_FAILURE':
                    response = HttpResponse(html + "Transaction Timeout")
                else:
                    response = HttpResponse(html + "success")
            else:
                response = HttpResponse(html + "Technical issue")

        except Exception as e:
            response = HttpResponse(html + "something went wrong!")

        return response


class PaytmTransactionInit(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'MID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter Merchant id here.'
                )
            ),
            coreapi.Field(
                'txn_amount',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter transaction amount here.'
                )
            ),
            coreapi.Field(
                'mobile',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter mobile here.'
                )
            ),
        ]
    )

    def post(self, request):
        try:
            data = request.data
            mid = data.get("MID")
            orderId = settings.ORDER_ID_PREFIX + Checksum.__id_generator__()

            body = {
                "orderId": orderId,
                "requestType": "Payment",
                "mid": mid,
                "userInfo": {
                    # "firstName": "test",
                    "mobile": data.get("mobile"),
                    # "lastName": "test",
                    "custId": "C11",
                    # "email": "test@gmail.com"
                },
                "txnAmount": {
                    "currency": "INR",
                    "value": str(round(float(data.get("txn_amount")), 2))
                },
                "websiteName": "DEFAULT",
                "callbackUrl": settings.PAYMENT_CALLBACK_BASE_URL+"/api/v1/verifychecksum/"
            }
            merchant_key = settings.MERCHANT_SECRET
            checksum = Checksum.generate_checksum_by_str(str(body).replace("'", '"'), merchant_key)
            print(checksum)
            head = {
                "version": "v1",
                # "requestTimestamp": int(datetime.now().strftime('%s'))*1000,
                "clientId": "C11",
                "signature": checksum,
                "channelId": "WAP"
            }

            request = {
                "head": head,
                "body": body
            }

            data = str(request).replace("'", '"')
            post_args = {
                'headers': {'Content-type': 'application/json'},
                'timeout': (10, 30),  # this connect timeout and read timeout in second
                'data': data
            }
            # for staging
            # url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=" + mid + "&orderId=" + orderId
            # for production
            url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=" + mid + "&orderId=" + orderId
            res = requests.post(url, **post_args)
            data = json.loads(res.content.decode('utf-8'))

            transaction_token = data['body']['txnToken']
            # print(data.get('body'))
            # print("request data  : {}".format(data))
            # print("response code: {} and response content : {}".format(res, res.content))
            response = Response({'message': "token created Successfully", 'status': True,
                                 'data': {'txnToken': transaction_token, "order_id": orderId}},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'message': 'Paytm Is not working please try later', 'status': False},
                                status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class TransactionN(APIView):
    # schema = schemas.ManualSchema(
    #     fields=[
    #         coreapi.Field(
    #             'MID',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter Merchant id here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'orderId',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter transaction amount here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'txnToken',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter mobile here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'channel_code',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='payment_mode'
    #             )
    #         )
    #
    #     ]
    # )

    def post(self, request):
        try:
            print(request.data)
            data = request.data
            MID = data.get("MID")
            orderId = data.get("orderId")
            txnToken = data.get("txnToken")
            paytmParams = dict()

            paytmParams["body"] = {
                "paymentMode": "NET_BANKING",
                "requestType": "NATIVE",
                "mid": MID,
                "orderId": orderId,
                "channelCode": data.get('channel_code'),
                "paymentFlow": "NONE",
                "storeInstrument": "0"
            }

            # url = "https://securegw-stage.paytm.in/theia/api/v1/" # for staging
            url = "https://securegw.paytm.in/theia/api/v1/"  # for production

            url = url + "processTransaction?mid=" + MID + "&orderId=" + orderId
            print(url)
            paytmParams["head"] = {
                "version": "v1",
                # "requestTimestamp" : str(int(time.time())),
                "channelId": "WEB",
                "txnToken": txnToken
            }

            post_data = json.dumps(paytmParams)
            response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
            # print(response['body']['bankForm'])
            direct_form = response['body']['bankForm']['redirectForm']
            print(direct_form)
            if direct_form['type'] == 'redirect':
                url = direct_form['actionUrl']
                content = direct_form.get('content', {})
                return Response({'message': 'Transaction bank page',
                                 'bankhtml': render_to_string("bankpage.html", {"paytmdict": content, "url": url}),
                                 'status': True}, status=http_status_codes.HTTP_200_OK)
                # return render(request, "bankpage.html", {"paytmdict": content, "url": url})
        except Exception as e:
            print(e)
            return Response({'message': 'Transaction error please check all fields and try later', 'status': False},
                            status=http_status_codes.HTTP_403_FORBIDDEN)


class TransactionP(APIView):
    # schema = schemas.ManualSchema(
    #     fields=[
    #         coreapi.Field(
    #             'MID',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter Merchant id here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'orderId',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter transaction amount here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'txnToken',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter mobile here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'card_type',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter Merchant id here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'card_no',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter transaction amount here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'cvv',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter mobile here.'
    #             )
    #         ),
    #         coreapi.Field(
    #             'expiry',
    #             required=True,
    #             location='form',
    #             schema=coreschema.String(
    #                 description='Enter mobile here.'
    #             )
    #         )
    #     ]
    # )

    def post(self, request):
        try:
            print(request.data)
            data = request.data
            MID = data.get("MID")
            orderId = data.get("orderId")
            txnToken = data.get("txnToken")
            paytmParams = dict()

            paytmParams["body"] = {
                "requestType": "NATIVE",
                "mid": MID,
                "orderId": orderId,
                "paymentMode": data.get("card_type"),
                "authMode": "otp",
                "cardInfo": "|{}|{}|{}".format(data.get("card_no"), data.get("cvv"), data.get("expiry")),
                "paymentFlow": "NONE",
                "storeInstrument": "0"
            }

            # url = "https://securegw-stage.paytm.in/theia/api/v1/" # for staging
            url = "https://securegw.paytm.in/theia/api/v1/"  # for production

            url = url + "processTransaction?mid=" + MID + "&orderId=" + orderId
            print(url)
            paytmParams["head"] = {
                "version": "v1",
                # "requestTimestamp" : str(int(time.time())),
                "channelId": "WEB",
                "txnToken": txnToken
            }

            post_data = json.dumps(paytmParams)
            response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()

            direct_form = response['body']['bankForm']['redirectForm']

            if direct_form['type'] == 'redirect':
                url = direct_form['actionUrl']
                content = direct_form.get('content', "")
                return Response({'message': 'Transaction bank page',
                                 'bankhtml': render_to_string("bankpage.html", {"paytmdict": content, "url": url}),
                                 'status': True}, status=http_status_codes.HTTP_200_OK)
                # return render(request, "bankpage.html", {"paytmdict": content, "url": url})
        except Exception as e:
            print(e)
            return Response({'message': 'Transaction error please check all fields and try later', 'status': False},
                            status=http_status_codes.HTTP_403_FORBIDDEN)


class TransactionDetail(APIView):
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'STATUS',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Status of transaction'
                )
            ),
            coreapi.Field(
                'CHECKSUMHASH',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Check sum hash'
                )
            ),

            coreapi.Field(
                'BANKNAME',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Bank Name for Transaction'
                )
            ),

            coreapi.Field(
                'ORDERID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='order id'
                )
            ),

            coreapi.Field(
                'TXNAMOUNT',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Transaction Amount'
                )
            ),

            coreapi.Field(
                'TXNDATE',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Transaction Date'
                )
            ),

            coreapi.Field(
                'MID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Merchant ID'
                )
            ),

            coreapi.Field(
                'TXNID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Transaction ID'
                )
            ),

            coreapi.Field(
                'RESPCODE',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Response code'
                )
            ),

            coreapi.Field(
                'PAYMENTMODE',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Mode of transaction'
                )
            ),

            coreapi.Field(
                'BANKTXNID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Bank transaction id'
                )
            ),

            coreapi.Field(
                'CURRENCY',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Currency'
                )
            ),

            coreapi.Field(
                'GATEWAYNAME',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Payment Gateway'
                )
            ),

            coreapi.Field(
                'RESPMSG',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Response message'
                )
            ),

        ])

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.data.pop("CHECKSUMHASH")
        PaymentHistory.objects.create(user_id=request.user.id, **request.data)
        return Response({'message': 'Transaction detail saved', 'status': True},
                        status=http_status_codes.HTTP_201_CREATED)


class TransactionStatus(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'MID',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter Merchant id here.'
                )
            ),
            coreapi.Field(
                'order_id',
                required=True,
                location='form',
                schema=coreschema.String(
                    description='Enter order id here.'
                )
            ),
        ]
    )

    def post(self, request):
        # initialize a dictionary
        try:
            paytmParams = dict()
            data = request.data
            paytmParams["MID"] = data.get("MID")

            # Enter your order id which needs to be check status for
            paytmParams["ORDERID"] = data.get("order_id")

            # Generate checksum by parameters we have in body
            # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            checksum = Checksum.generate_checksum(paytmParams, settings.MERCHANT_SECRET)
            # print(checksum)
            # put generated checksum value here
            paytmParams["CHECKSUMHASH"] = checksum

            # prepare JSON string for request
            post_data = json.dumps(paytmParams)

            # for Staging
            # url = "https://securegw-stage.paytm.in/order/status"

            # for Production
            url = "https://securegw.paytm.in/order/status"
            res = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
            # print(res)

            response = Response({"message": "transaction status ", "data": res}, status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({'message': 'Paytm Is not working please try later', 'status': False},
                                status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
