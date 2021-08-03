from rest_framework import serializers
from apps.common.models import Page,ContactPage,Faqs


class PageAboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['title', 'content']


class PageContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['title', 'content']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        fields = ['whatsapp_number', 'email']


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faqs
        fields = '__all__'