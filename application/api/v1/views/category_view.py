from apps.stores.models import Category
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.serializers.category_serializer import KitchenCategorySerializer
from rest_framework import status as http_status_codes


class CategoryListView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk,is_deleted = False)
            serializer = KitchenCategorySerializer(category)
            response = Response({ 'status': True, 'data': serializer.data},
                                status=http_status_codes.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = Response({'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        return response
