from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from config import settings
from libraries.Functions import generate_password
from libraries.Email_templates import get_owner_registration_verify_content
from libraries.Email_model import send_auth_email
from apps.users.models import User, Group
from libraries.DataTables import DataTables
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
# from django.contrib.auth.mixins import LoginRequiredMixin
from pkbadmin.forms.client_forms import ClientForm,UpdateClientForm
from pkbadmin.views.decorators import GroupRequiredMixin
from django.views import View
from django.core import signing
from django.db import transaction


class ClientIndex(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'clients/index.html'

    def get(self, request):
        """
                function for getting group html page
                :param request:
                :return html page:
                """
        return render(request, self.template_name)


class ClientGet(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        # user = User.objects.get(is_superuser=False, is_active=True,created_by = request.user.id)
        user = User.objects.filter(is_superuser=False, is_active=True, created_by=request.user.id, groups__name='Owner')
        # print(user.query)
        datatable = DataTables(request, User)
        datatable.COLUMN_SEARCH = ['name', 'email', 'mobile']
        datatable.select('id', 'name', 'email', 'mobile')
        datatable.set_queryset(user)
        return datatable.response()


class AddClient(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = ClientForm()

    template_name = 'clients/create.html'

    def get(self, request):

        form_class = ClientForm()
        form = form_class
        roles = Group.objects.get(name='Owner')
        return render(request, self.template_name, {'form': form_class, 'form_errors': form.errors, "groups": roles})

    def post(self, request):
        form_class = ClientForm(request.POST)
        roles = Group.objects.get(name='Owner')
        form = form_class

        if form.is_valid():
            validated_data = {}
            temp_password = generate_password()
            role = request.POST.get('role')
            group = Group.objects.get(id=role)

            validated_data['username'] = form.cleaned_data['email']
            validated_data['name'] = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
            validated_data['first_name'] = form.cleaned_data['first_name']
            validated_data['last_name'] = form.cleaned_data['last_name']
            validated_data['email'] = form.cleaned_data['email']
            validated_data['mobile'] = form.cleaned_data['mobile']
            validated_data['gender'] = request.POST.get('gender')
            validated_data['dob'] = request.POST.get('dob')
            validated_data['password'] = make_password(temp_password)
            validated_data['is_staff'] = 0
            validated_data['is_superuser'] = 0
            validated_data['is_email_verified'] = 0
            validated_data['updated_on'] = timezone.now()
            validated_data['created_by_id'] = request.user.id

            with transaction.atomic():
                user = User.objects.create(**validated_data)
                group.user_set.add(user)

            if user:
                token_data = {
                    'id': user.id,
                    'email': user.email
                }
                token = signing.dumps(token_data)
                link = (settings.BASE_URL, 'admin/register-verify/?token=', token)
                link = ''.join(link)
                data = {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_name': user.email,
                    'password': temp_password,
                    'link': link
                }
                body = get_owner_registration_verify_content(request, data)
                receiver = user.email
                subject = "Registration Verification Mail"

                send_auth_email(subject, body, receiver)

            return HttpResponseRedirect(reverse('custom-admin:client_index'))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors, "groups": roles})


class UpdateClient(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = UpdateClientForm
    fields = ['first_name', 'last_name']

    initial = {"key": "value"}
    template_name = 'clients/create.html'

    def get(self, request, pk):
        obj = User.objects.get(pk=pk)
        form = self.form_class(obj.__dict__,initial={'pk': pk})
        roles = Group.objects.get(name='Owner')

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors, "groups": roles})

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES,initial={'pk': pk})
        roles = Group.objects.get(name='Owner')

        if form.is_valid():
            user = User.objects.get(pk=pk)
            user.username = form.cleaned_data['email']
            user.name = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.mobile = form.cleaned_data['mobile']
            user.gender = request.POST.get('gender')
            user.dob = request.POST.get('dob')
            user.save()
            return HttpResponseRedirect(reverse('custom-admin:client_index'))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors,"groups": roles})


class DetailClient(GroupRequiredMixin, View):
    group_required = ['Super admin']

    template_name = 'clients/detail.html'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)

        return render(request, self.template_name, {'client': user})


class DeleteClient(GroupRequiredMixin, APIView):
    group_required = ['Super admin']

    def get(self, request, pk):
        """
        Delete a Client as soft delete. Will update the is_active field = False from user table
        :param request:
        :return Json response:
        """
        User.objects.filter(pk=pk).update(is_active=False)

        return Response({"status": True, 'message': "Client Successfully Deleted!"})
