# import requests
# from datetime import datetime
# from libraries.Paytm import Checksum
#
# mid = "wPnEhs24887802658211"
#
# orderId = Checksum.__id_generator__()
#
# body = {
#     "orderId": orderId,
#     "requestType": "Payment",
#     "mid": mid,
#     "userInfo": {
#         "firstName": "Abhishek",
#         "mobile": "9720457881",
#         "lastName": "soni",
#         "pincode": "201301",
#         "address": "strtype",
#         "custId": "cid",
#         "email": "abhi@gmail.com"
#     },
#     "txnAmount": {
#         "currency": "INR",
#         "value": "1.00"
#     },
#     "websiteName": "WEBSTAGING",
#     "callbackUrl": "http://139.59.14.145/api/v1/verifychecksum/"
# }
# merchant_key = "KjN&28_FsEEUmShz"
# checksum = Checksum.generate_checksum_by_str(str(body).replace("'", '"'), merchant_key)
# head = {
#     "version": "v2",
#     # "requestTimestamp": str(datetime.now()),
#     "clientId": "C11",
#     "signature": checksum.decode('utf-8')
# }
#
# request = {
#     "head": head,
#     "body": body
# }
#
# data = str(request).replace("'", '"')
# post_args = {
#     'headers': {'Content-type': 'application/json'},
#     'timeout': (10, 30),  # this connect timeout and read timeout in second
#     'data': data
# }
# # for staging
# url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=" + mid + "&orderId=" + orderId
# print(url)
# # for production
# # url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=" + mid + "&orderId=" + orderId
# res = requests.post(url, **post_args)
# print("request data  : {}".format(data))
# print("response code: {} and response content : {}".format(res, res.content))
