from django.urls import reverse
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from libraries.DataTables import DataTables
from apps.common.models import ContactPage as Contact
# from django.views.generic.edit import CreateView, UpdateView
from pkbadmin.forms.contact_forms import ContactForm
from django.views import View
# from django.views import generic
from django.http import HttpResponseRedirect
from pkbadmin.views.decorators import GroupRequiredMixin


class ContactIndex(GroupRequiredMixin, View):
    template_name = 'contact/index.html'
    group_required = ['Super admin']

    def get(self, request):
        """
        function for getting group html page
        :param request:
        :return html page:
        """
        return render(request, self.template_name)


class ContactGet(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        qs = Contact.objects.all()
        datatable = DataTables(request, Contact)
        datatable.COLUMN_SEARCH = ['contact_address', 'whatsapp_number', 'paytm_number', 'email']
        datatable.select('id', 'contact_address', 'timing', 'whatsapp_number', 'paytm_number', 'email', 'status')
        datatable.set_queryset(qs)

        return datatable.response()


class AddContact(GroupRequiredMixin, View):
    group_required = ['Super admin']

    form_class = ContactForm
    initial = {"key": "value"}
    template_name = 'contact/create.html'

    def get(self, request):

        form = self.form_class(initial=self.initial)

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            Contact.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse('custom-admin:contact_index'))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class UpdateContact(GroupRequiredMixin, View):
    group_required = ['Super admin']

    form_class = ContactForm
    initial = {"key": "value"}
    template_name = 'contact/create.html'

    def get(self, request, pk):
        obj = Contact.objects.get(pk=pk)
        form = self.form_class(initial=obj.__dict__)
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            Contact.objects.filter(pk=pk).update(**form.cleaned_data)
            return HttpResponseRedirect(reverse('custom-admin:contact_index'))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class DeleteContact(GroupRequiredMixin, APIView):
    group_required = ['Super admin']

    def get(self, request, pk):
        Contact.objects.filter(pk=pk).delete()
        return Response({"status": True, 'message': "Contact Successfully Deleted!"})

