from django.contrib import messages
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from apps.users.models import User, Group
from libraries.DataTables import DataTables
from django.http import HttpResponseRedirect, JsonResponse
from pkbadmin.forms.delivery_forms import DeliveryForm, DeliveryUpdateForm
from django.views import View
from apps.stores.models import Store, Kitchen, StoreManager,KitchenDelivery
from pkbadmin.views.decorators import GroupRequiredMixin
from django.db import transaction
from config import settings
from libraries.Email_model import send_auth_email
from libraries.Email_templates import get_manager_registration_verify_content
from libraries.Functions import generate_password
from django.core.validators import validate_email
from django.core import signing
from django.utils import timezone
from django.contrib.auth import hashers

class DeliveryIndex(GroupRequiredMixin, View):
    group_required = ['Manager']
    template_name = 'delivery/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetDelivery(GroupRequiredMixin, View):
    group_required = ['Manager']

    def post(self, request):
        qs = User.objects.filter(is_superuser=False, groups__name='Delivery boy',created_by=request.user.id,is_active=True)

        m = Group.objects.all()
        # print(m)
        datatable = DataTables(request, User)
        datatable.COLUMN_SEARCH = ['name', 'email', 'mobile']
        datatable.select('id', 'name', 'email', 'mobile', 'is_active')
        datatable.set_queryset(qs)

        return datatable.response()


class AddDelivery(GroupRequiredMixin, View):
    group_required = ['Manager']

    form_class = DeliveryForm
    initial = {"key": "value"}

    template_name = 'delivery/create.html'

    def get(self, request):
        kitchen = request.user.kitchenmanager.kitchen
        form_class = self.form_class(initial=self.initial)
        groups = Group.objects.filter(name='Delivery boy')
        return render(request, self.template_name,
                      {'form': form_class, 'form_errors': form_class.errors, "groups": groups,'kitchen':kitchen })

    def post(self, request):
        form_class = self.form_class(request.POST, initial={'user': request.user})
        form = form_class
        groups = Group.objects.filter(name='Delivery boy')
        mobile = request.POST.get('mobile')
        kitchen = request.user.kitchenmanager.kitchen.id
        if form.is_valid():
            with transaction.atomic():
                try:
                    delivery = User.objects.get(mobile=mobile) //"""if user already exists with this mobile number"""
                except Exception as e:
                    delivery = User.objects.create(mobile=mobile,username=mobile)
                    group = Group.objects.get(name__exact="User")
                    group.user_set.add(delivery)
                    group.save()
                delivery.username = request.POST.get('mobile')
                delivery.first_name = request.POST.get('first_name')
                delivery.last_name = request.POST.get('last_name')
                delivery.name = request.POST.get('first_name') + request.POST.get('last_name')
                delivery.email = request.POST.get('email')
                delivery.mobile = request.POST.get('mobile')
                delivery.gender = request.POST.get('gender')
                delivery.updated_on = timezone.now()
                delivery.dob = request.POST.get('dob')
                if delivery:
                    token_data = {
                        'id': delivery.id,
                        'email': delivery.email
                    }
                    token = signing.dumps(token_data)
                    link = (settings.BASE_URL, 'admin/register-verify/?token=', token)
                    link = ''.join(link)
                    temp_password = generate_password()
                    data = {
                        'email': delivery.email,
                        'first_name': delivery.first_name,
                        'last_name': delivery.last_name,
                        'user_name': delivery.email,
                        'password': temp_password,
                        'link': link
                    }

                    body = get_manager_registration_verify_content(data)
                    receiver = delivery.email
                    subject = "Registration Verification Mail"
                    send_auth_email.delay(subject, body, receiver)

                KitchenDelivery.objects.create(kitchen_id=int(kitchen), deliver_boy_id=int(delivery.id))
                manager_group = Group.objects.get(name='Delivery boy')
                # user_group = User.groups.through.objects.get(user=user)
                # user_group.group = manager
                # user_group.save()
                # group.save()
                # delivery.password = hashers.make_password(temp_password)
                manager_group.user_set.add(delivery)
                delivery.created_by = request.user
                delivery.save()
            return HttpResponseRedirect(reverse("custom-admin:delivery_index"))

        return render(request, self.template_name,
                      {'form': form, 'form_errors': form.errors, "groups": groups, })


class UpdateDelivery(GroupRequiredMixin, View):
    group_required = ['Manager']
    form_class = DeliveryUpdateForm
    fields = ['first_name', 'last_name']

    initial = {"key": "value"}
    template_name = 'delivery/edit.html'

    def get(self, request, pk):
        obj = User.objects.get(id=pk)
        form = self.form_class(initial=obj.__dict__)
        groups = Group.objects.filter(name='Delivery boy')

        return render(request, self.template_name,
                      {'form': form, 'form_errors': form.errors, "groups": groups, })

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        form = self.form_class(request.POST, initial={'pk': pk})
        groups = Group.objects.filter(name='Deliver boy')
        if form.is_valid():
            user.name = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.name = request.POST.get('first_name') + request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.mobile = request.POST.get('mobile')
            user.gender = request.POST.get('gender')
            user.updated_on = timezone.now()
            user.dob = request.POST.get('dob')
            user.created_by = request.user
            user.save()

            return HttpResponseRedirect(reverse("custom-admin:delivery_index"))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors, "groups": groups})


class DeactivateDelivery(GroupRequiredMixin, APIView):
    group_required = ['Manager']

    def get(self, request, pk):
        User.objects.filter(pk=pk).update(is_active=False)
        # StoreManager.objects.filter(manager_id=pk).delete()
        return Response({"status": True, 'message': "Delivery boy status changed successfully."})


class DeliveryProfile(GroupRequiredMixin, View):
    group_required = ['Manager']

    template_name = 'delivery/profile.html'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return render(request, self.template_name,
                      {'delivery': user})
