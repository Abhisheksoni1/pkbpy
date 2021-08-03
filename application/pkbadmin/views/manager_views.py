from django.contrib.auth import hashers
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from apps.users.models import User, Group
from libraries.DataTables import DataTables
from django.http import HttpResponseRedirect, JsonResponse
from pkbadmin.forms.manager_forms import ManagerForm, ManagerUpdateForm
from django.views import View
from apps.stores.models import Store, Kitchen, StoreManager, KitchenManager, StoreOwner
from pkbadmin.views.decorators import GroupRequiredMixin
from django.forms import model_to_dict
from django.db import transaction
from config import settings
from libraries.Email_model import send_auth_email
from libraries.Email_templates import get_manager_registration_verify_content
from libraries.Functions import generate_password
from django.core.validators import validate_email
from django.core import signing


class ManagerIndex(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner']
    template_name = 'managers/index.html'

    def get(self, request):
        try:
            store = StoreOwner.objects.get(owner=request.user)
            store_id = store.store.id
            stores = Kitchen.objects.filter(store_id=store_id)
            stores = [store for store in stores if store.managers.count() == 0]
            return render(request, self.template_name, {'stores': stores})
        except Exception as e:
            messages.error(request, "Please add Store first.", extra_tags="")
            return HttpResponseRedirect(reverse("custom-admin:index"))


class GetManager(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner']

    def post(self, request):
        if request.user.is_superuser:
            qs = User.objects.filter(is_superuser=False, groups__name='Manager')
            datatable = DataTables(request, User)
            datatable.COLUMN_SEARCH = ['name', 'email', 'mobile']
            datatable.select('id', 'name', 'email', 'mobile', 'is_active')
            datatable.set_queryset(qs)
            return datatable.response()
        elif request.user.storeowner:
            qs = User.objects.filter(is_superuser=False, groups__name='Manager', created_by=request.user.id)
            datatable = DataTables(request, User)
            datatable.COLUMN_SEARCH = ['name', 'email', 'mobile']
            datatable.select('id', 'name', 'email', 'mobile', 'is_active')
            datatable.set_queryset(qs)
            return datatable.response()


class AddManager(GroupRequiredMixin, View):
    group_required = ['Owner']
    form_class = ManagerForm
    initial = {"key": "value"}
    template_name = 'managers/create.html'

    def get(self, request):
        form_class = self.form_class(initial=self.initial)
        groups = Group.objects.filter(name='Manager')

        store_id = self.request.user.storeowner.store.id
        kitchens = Kitchen.objects.filter(store_id=store_id, is_deleted=False)
        kitchens_remain = [kitchen for kitchen in kitchens if kitchen.managers.count() == 0]
        if kitchens_remain:
            return render(request, self.template_name,
                          {'form': form_class, 'form_errors': form_class.errors, "groups": groups,
                           "kitchens": kitchens_remain})
        else:
            messages.error(request, "Please add kitchen first.", extra_tags="")
            return HttpResponseRedirect(reverse("custom-admin:manager_index"))

    def post(self, request):
        form_class = self.form_class(request.POST, initial={'user': request.user})
        form = form_class
        groups = Group.objects.filter(name='Manager')
        store_id = self.request.user.storeowner.store.id
        kitchen = Kitchen.objects.filter(store_id=store_id, is_deleted=False)
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        if form.is_valid():
            with transaction.atomic():
                try:
                    manager = User.objects.get(mobile=mobile)
                except Exception as e:
                    manager = User.objects.create(mobile=mobile, username=mobile)
                    group = Group.objects.get(name__exact="User")
                    group.user_set.add(manager)
                    group.save()
                manager.username = request.POST.get('mobile')
                manager.first_name = request.POST.get('first_name')
                manager.last_name = request.POST.get('last_name')
                manager.name = request.POST.get('first_name') + request.POST.get('last_name')
                manager.email = request.POST.get('email')
                manager.mobile = request.POST.get('mobile')
                manager.gender = request.POST.get('gender')
                manager.updated_on = timezone.now()
                manager.dob = request.POST.get('dob')
                if manager:
                    token_data = {
                        'id': manager.id,
                        'email': manager.email
                    }
                    token = signing.dumps(token_data)
                    link = (settings.BASE_URL, 'admin/register-verify/?token=', token)
                    link = ''.join(link)
                    temp_password = generate_password()
                    data = {
                        'email': manager.email,
                        'first_name': manager.first_name,
                        'last_name': manager.last_name,
                        'user_name': manager.email,
                        'password': temp_password,
                        'link': link
                    }

                    body = get_manager_registration_verify_content(data)
                    receiver = manager.email
                    subject = "Registration Verification Mail"
                    send_auth_email.delay(subject, body, receiver)
                manager_group = Group.objects.get(name='Manager')
                # user_group = User.groups.through.objects.get(user=user)
                # user_group.group = manager
                # user_group.save()
                # group.save()
                manager.password = hashers.make_password(temp_password)
                manager_group.user_set.add(manager)
                manager.created_by = request.user
                manager.save()
                KitchenManager.objects.create(kitchen_id=int(request.POST.get('kitchen')), manager_id=int(manager.id))
                return HttpResponseRedirect(reverse("custom-admin:manager_index"))
        else:
            return render(request, self.template_name,
                          {'form': form, 'form_errors': form.errors, "groups": groups, "kitchens": kitchen,
                           'gender': gender})


class UpdateManager(GroupRequiredMixin, View):
    group_required = ['Owner']
    form_class = ManagerUpdateForm
    fields = ['first_name', 'last_name']

    initial = {"key": "value"}
    template_name = 'managers/edit.html'

    def get(self, request, pk):
        obj = User.objects.get(id=pk)
        # print(model_to_dict(obj))
        form = self.form_class(model_to_dict(obj), initial={'pk': pk})
        groups = Group.objects.filter(name='Manager')
        try:
            kitchen_selected = Kitchen.objects.get(manager__manager_id=pk)
            kitchens = Kitchen.objects.filter(store_id=request.user.storeowner.store.id, is_deleted=False)
            kitchen_remain = [kitchen for kitchen in kitchens if kitchen.managers.count() == 0]
            kitchen_remain.append(kitchen_selected)
            return render(request, self.template_name,
                          {'form': form, 'form_errors': form.errors, "groups": groups, 'kitchens': kitchens,
                           'kitchen_selected': kitchen_selected.id, 'gender': obj.gender, 'dob': obj.dob,'manager':pk})
        except Exception as e:
            print(e)
            messages.error(request, "Please add store first.", extra_tags="")
            return HttpResponseRedirect(reverse("custom-admin:manager_index"))

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        form = self.form_class(request.POST, initial={'pk': pk, 'Gender': user.gender})
        # print(request.POST)
        groups = Group.objects.filter(name='Manager')
        kitchen_id = request.POST.get('kitchen')
        kitchen_selected = Kitchen.objects.get(id=kitchen_id)
        kitchens = Kitchen.objects.filter(store_id=request.user.storeowner.store.id, is_deleted=False)
        kitchen_remain = [kitchen for kitchen in kitchens if kitchen.managers.count() == 0]
        kitchen_remain.append(kitchen_selected)

        if form.is_valid():
            with transaction.atomic():
                # user =  User.objects.get(id=pk)
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

                KitchenManager.objects.filter(manager_id=pk).update(kitchen_id=int(kitchen_id))

            return HttpResponseRedirect(reverse("custom-admin:manager_index"))
        return render(request, self.template_name,
                      {'form': form, 'form_errors': form.errors, "groups": groups, 'kitchens': kitchen_remain,
                       'kitchen_selected': kitchen_selected.id, 'gender': user.gender, 'dob': user.dob,'manager':pk})


class DeactivateManager(GroupRequiredMixin, APIView):
    group_required = ['Super admin', 'Owner']

    def get(self, request, pk):
        User.objects.filter(pk=pk).update(is_active=False)
        KitchenManager.objects.filter(manager_id=pk).delete()
        return Response({"status": True, 'message': "Manager status changed successfully."})


class ManagerProfile(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner']

    template_name = 'managers/manager_profile.html'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return render(request, self.template_name,
                      {'manager': user})


class GetStores(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner']

    def post(self, request):
        manager_id = request.POST.get('manager_id')
        user = request.user

        if user.is_superuser:

            qs = Store.objects.filter(is_deleted=False, manager__manager_id=manager_id)

        else:
            store = request.user.storeowner.store.id
            qs = Store.objects.filter(id=store, is_deleted=False)

        datatable = DataTables(request, Store)
        datatable.COLUMN_SEARCH = ['name', 'tag_line', 'description', 'address']
        datatable.select('id', 'name', 'tag_line', 'description', 'address', 'status')
        datatable.set_queryset(qs)

        return datatable.response()


class GetKitchens(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner']

    def post(self, request):
        user = User.objects.get(id=request.POST.get('manager_id'))
        if user.is_active:
            manager_id = request.POST.get('manager_id')
            kitchen = KitchenManager.objects.get(manager_id=int(manager_id)).kitchen
            qs = Kitchen.objects.filter(is_deleted=False, id=kitchen.id)
        else:
            qs=Kitchen.objects.none()
        datatable = DataTables(request, Kitchen)
        datatable.COLUMN_SEARCH = ['name', 'tag_line', 'description', 'address']
        datatable.select('id', 'name', 'tag_line', 'description', 'address', 'store_id__name',
                         'status')
        datatable.set_queryset(qs)

        return datatable.response()


class UpdateManagerStatus(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner']

    def post(self, request):
        kitchen_id = request.POST.get('store_id')
        manager_id = request.POST.get('manager_id')

        User.objects.filter(id=manager_id).update(is_active=True)
        KitchenManager.objects.create(
            kitchen_id=kitchen_id,
            manager_id=manager_id,
        )
        return JsonResponse({'status': True, 'message': 'Manager assigned a store.'})
