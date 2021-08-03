from api.v1.serializers.auth_serializer import MyTokenObtainPairSerializer
from apps.users.models import User
from rest_framework.views import Response
from rest_framework import status as http_status_codes
from functools import wraps
from django.contrib.auth import get_user_model

def get_my_token(user_detail):
    my_token = MyTokenObtainPairSerializer()
    data = my_token.validate(user_detail)
    return data

# def jwt_check(func,**kwargs):
#     def decorated(class_obj, *args, **kwargs):
#
#         try:
#             request_token = class_obj.request.META['HTTP_AUTHORIZATION']
#             if class_obj.request.user.is_superuser == 1:
#
#                 print('******')
#                 print(class_obj.request.user.get_all_module_actions)
#                 print(class_obj.request.user.get_all_modules)
#                 print(class_obj.request.user.get_all_roles)
#                 print('******')
#
#                 return func(class_obj, *args, **kwargs)
#             else:
#                 return Response({'message': 'you are not authorized to this url', 'data': {}},
#                                 status=http_status_codes.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'message': 'please login first to access url', 'data': {}},
#                         status=http_status_codes.HTTP_400_BAD_REQUEST)
#         return func(class_obj,*args,**kwargs)
#     return decorated

class jwt_check(object):

    def __call__(self, func, *args, **kwargs):

        def wrap(class_obj, *args, **kwargs):
            try:
                #request_token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
                request_token = class_obj.request.META.get('HTTP_AUTHORIZATION',None)
                if not request_token:
                    return Response({'message': 'please login first to access url', 'data': {}},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'you are not authorized to this url (permission denied)', 'data': {}},
                                        status=http_status_codes.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': 'Server error.', 'error': {'error':str(e)}, 'data': {}},
                            status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)

        return wrap


