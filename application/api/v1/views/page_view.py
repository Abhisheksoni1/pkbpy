from rest_framework.views import APIView
from rest_framework import status as http_status_codes
from apps.common.models import Page, ContactPage, Faqs
from api.v1.serializers.page_serializer import PageAboutUsSerializer, PageContactUsSerializer, ContactUsSerializer, \
    FaqSerializer
from rest_framework.response import Response


class AboutUsView(APIView):

    def get(self, request):
        try:
            page = Page.objects.get(title='About-Us')

            serializer = PageAboutUsSerializer(page).data

            response = Response({'message': "About-Us detail", 'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)

            response = Response({'message': "No data found", 'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        return response


class ContactUsView(APIView):

    def get(self, request):
        try:
            page = ContactPage.objects.get(id=1)

            serializer = ContactUsSerializer(page).data

            response = Response({'message': "contact-Us detail", 'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)

            response = Response({'message': "No data found", 'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        return response


class Privacy(APIView):

    def get(self, request):
        try:
            page = Page.objects.get(title='Privacy-Policy')

            serializer = PageContactUsSerializer(page).data

            response = Response({'message': "Privacy detail", 'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)

            response = Response({'message': "No data found ", 'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        return response


class TermOfUse(APIView):

    def get(self, request):
        try:
            page = Page.objects.get(title='Term-of-Use')

            serializer = PageContactUsSerializer(page).data

            response = Response({'message': "Term of use detail", 'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)

            response = Response({'message': "No data found", 'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        return response


class Cancellation(APIView):

    def get(self, request):
        try:
            page = Page.objects.get(title='Cancellation and Refund Policy')
            serializer = PageContactUsSerializer(page).data
            response = Response({'message': "Cancellation and Refund Policy", 'status': True, 'data': serializer},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)

            response = Response({'message': "No data found", 'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)
        return response


class FaqsView(APIView):
    def get(self, request):
        try:
            faqs = Faqs.objects.filter(is_deleted=False)
            serializer = FaqSerializer(faqs, many=True)
            response = Response({'message': "Faqs PKB", 'status': True, 'data': serializer.data},
                                status=http_status_codes.HTTP_200_OK)
        except Exception as e:
            print(e)

            response = Response({'message': "No data found", 'status': False, 'data': []},
                                status=http_status_codes.HTTP_200_OK)

        return response