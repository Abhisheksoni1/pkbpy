from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render
from django.urls import reverse

from config import settings
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from pkbadmin.forms.categories_form import CategoryManagementForm, UpdateCategory
from libraries.Functions import image_upload_handler, make_dir, join_string
from apps.stores.models import Category, Store
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from libraries.DataTables import DataTables
# from pkbadmin.forms.promo_banner_forms import PromoForm
# from apps.common.models import PromoBanner
from apps.stores.models import Kitchen
import os
from pkbadmin.views.decorators import GroupRequiredMixin


class CategoryIndex(GroupRequiredMixin, View):
    template_name = 'categories/index.html'
    group_required = ['Manager', 'Owner']

    def get(self, request):
        """
        function for getting group html page
        :param request:
        :return html page:
        """
        return render(request, self.template_name)


class CategoryGet(GroupRequiredMixin, View):
    group_required = ['Manager', 'Owner']

    def post(self, request):
        if request.user.is_superuser:
            data = Category.objects.filter(is_deleted=False, status=True)
            # data = Category.objects.all()
            datatable = DataTables(request, Category)
            datatable.COLUMN_SEARCH = ['name', 'kitchen_id__name']
            datatable.select('id', 'name', 'description', 'kitchen_id', 'kitchen_id__name',
                             'kitchen_id__store_id__name')
            datatable.set_queryset(data)

            return datatable.response()
        elif 'Owner' in request.user.group_name:
            data = Category.objects.filter(is_deleted=False, status=True,
                                           kitchen__store_id=request.user.storeowner.store.id)
            # data = Category.objects.all()
            datatable = DataTables(request, Category)
            datatable.COLUMN_SEARCH = ['name', 'kitchen_id__name']
            datatable.select('id', 'name', 'description', 'kitchen_id', 'kitchen_id__name',
                             'kitchen_id__store_id__name')
            datatable.set_queryset(data)

            return datatable.response()
        elif 'Manager' in request.user.group_name:
            data = Category.objects.filter(is_deleted=False, status=True,
                                           kitchen_id=request.user.kitchenmanager.kitchen.id)
            # data = Category.objects.all()
            datatable = DataTables(request, Category)
            datatable.COLUMN_SEARCH = ['name', 'kitchen_id__name']
            datatable.select('id', 'name', 'description', 'kitchen_id', 'kitchen_id__name',
                             'kitchen_id__store_id__name')
            datatable.set_queryset(data)

            return datatable.response()


class AddCategory(GroupRequiredMixin, View):
    group_required = ['Owner', 'Manager']
    form_class = CategoryManagementForm
    initial = {"key": "value"}
    template_name = 'categories/create.html'

    def get(self, request):
        if 'Owner' in request.user.group_name:
            store = self.request.user.storeowner.store.id
            form = self.form_class(self.initial, {'store': store})
            return render(request, self.template_name, {'form': form, 'errors': form.errors})
        else:
            kitchen = Kitchen.objects.get(manager__manager=request.user)
            store = kitchen.store.id
            form = self.form_class(self.initial, {'store': store, 'kitchen': kitchen.id})
            return render(request, self.template_name, {'form': form, 'errors': form.errors})

    def post(self, request):
        if 'Owner' in request.user.group_name:
            store = self.request.user.storeowner.store.id
        else:
            kitchen = Kitchen.objects.get(manager__manager=request.user)
            store = kitchen.store.id

        form = CategoryManagementForm(request.POST, {'store': store}, request.FILES)
        if form.is_valid():
            """create directory for category"""
            kitchen = int(form.cleaned_data['kitchen'])
            cat = Category.objects.filter(kitchen__id=kitchen, is_deleted=False).values_list('name', flat=True)
            name = form.cleaned_data['name']
            if not name in cat:
                kitchen_id_dir = int(form.cleaned_data['kitchen'])
                kitchen_obj = Kitchen.objects.get(pk=kitchen_id_dir)
                kitchen_name, store_name = join_string(kitchen_obj.name), join_string(kitchen_obj.store.name)
                directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
                img_path = os.path.join(directory, store_name,
                                        settings.CUSTOM_DIRS['KITCHEN_DIR'],
                                        kitchen_name,
                                        )

                category_name = form.cleaned_data['name']
                category_name = join_string(category_name)

                dir_name = make_dir(img_path + '/' +
                                    settings.CUSTOM_DIRS['CATEGORY_DIR'] +
                                    category_name + '/'
                                    + settings.CUSTOM_DIRS['IMAGE_DIR'])
                category = Category.objects.create(name=form.cleaned_data['name'],
                                                   description=form.cleaned_data['description'],
                                                   short_description=form.cleaned_data['short_description'],
                                                   status=form.cleaned_data['status'],
                                                   kitchen_id=int(form.cleaned_data['kitchen']),
                                                   created_on=timezone.now(),
                                                   created_by_id=request.user.id
                                                   )

                if request.FILES:
                    img_path = image_upload_handler(request.FILES['image'], dir_name)
                    full_path = "{}".format(img_path)
                    category.image = full_path
                    image_thumb = "{}".format("T_" + full_path)
                    category.image_thumb = image_thumb
                    category.save()

                return HttpResponseRedirect(reverse('custom-admin:categories'))
            else:
                name_error = 'This category name has been already taken.'
                return render(request, self.template_name, {'form': form,
                                                            'errors': form.errors, 'name_error': name_error})
        else:
            return render(request, self.template_name, {'form': form,
                                                        'errors': form.errors})


class UpdateCategory(GroupRequiredMixin, View):
    group_required = ['Manager', 'Owner']
    form_class = UpdateCategory
    initial = {"key": "value"}
    template_name = 'categories/edit.html'

    def get(self, request, pk):
        obj = Category.objects.get(pk=pk)
        form = self.form_class(model_to_dict(obj))
        store = obj.kitchen.store
        kitchen = obj.kitchen
        directory = settings.CUSTOM_DIRS['STORE_DIR'] + join_string(obj.kitchen.store.name) + "/" + \
                    settings.CUSTOM_DIRS['KITCHEN_DIR'] + join_string(obj.kitchen.name) \
                    + "/" + settings.CUSTOM_DIRS['CATEGORY_DIR'] + join_string(obj.name) + "/" + settings.CUSTOM_DIRS[
                        'IMAGE_DIR']

        return render(request, self.template_name,
                      {'form': form, 'errors': form.errors, 'store_id': obj.kitchen.store_id, "image_path": obj.image,
                       "directory": directory, "store": store, "kitchen": kitchen
                       })

    def post(self, request, pk):
        obj = Category.objects.get(pk=pk)
        store = obj.kitchen.store
        kitchen = obj.kitchen
        kitchen_id = Category.objects.get(pk=pk).kitchen.id
        cat = Category.objects.filter(~Q(id=pk),kitchen__id=kitchen_id, is_deleted=False).values_list('name', flat=True)
        form = self.form_class(request.POST, request.FILES)
        old_image = request.POST.get('old_image')
        directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + join_string(
            obj.kitchen.store.name) + "/" + \
                    settings.CUSTOM_DIRS['KITCHEN_DIR'] + join_string(obj.kitchen.name) \
                    + "/" + settings.CUSTOM_DIRS['CATEGORY_DIR']
        if form.is_valid():
            """create directory for category"""
            name = form.cleaned_data['name']
            if not name in cat:
                category = Category.objects.get(pk=pk)

                directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + join_string(
                    category.kitchen.store.name) + "/" + \
                            settings.CUSTOM_DIRS['KITCHEN_DIR'] + join_string(category.kitchen.name) \
                            + "/" + settings.CUSTOM_DIRS['CATEGORY_DIR']

                os.rename(directory + join_string(category.name), directory + join_string(form.cleaned_data['name']))

                dir_name = os.path.join(directory, join_string(form.cleaned_data['name']),
                                        settings.CUSTOM_DIRS['IMAGE_DIR'])

                img_path = image_upload_handler(request.FILES.get('image', None), dir_name)

                Category.objects.filter(pk=pk).update(name=form.cleaned_data['name'],
                                                      description=form.cleaned_data['description'],
                                                      short_description=form.cleaned_data['short_description'],
                                                      status=form.cleaned_data['status'],
                                                      image="{}".format(img_path) if img_path else old_image,
                                                      image_thumb=("{}".format(
                                                          "T_" + img_path)) if img_path else "T_" + old_image,
                                                      updated_on=timezone.now(),
                                                      created_by_id=request.user.id
                                                      )

                return HttpResponseRedirect(reverse('custom-admin:categories'))
            else:
                name_error = 'This category name has been already taken '
                return render(request, self.template_name,
                              {'form': form, 'errors': form.errors, 'store_id': obj.kitchen.store_id,
                               "image_path": obj.image,
                               "directory": directory, "store": store, "kitchen": kitchen, 'name_error': name_error
                               })

        return render(request, self.template_name, {'form': form, 'errors': form.errors})


class DeleteCategory(GroupRequiredMixin, APIView):
    group_required = ['Manager', 'Owner']

    def get(self, request, pk):
        Category.objects.filter(pk=pk).update(is_deleted=True)
        return Response({"status": True, 'message': "Category deleted successfully!"})


class GetStoreKitchen(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner']

    def post(self, request):
        store_id = request.POST.get('store_id')
        response = {'status': False, 'msg': '', 'data': {}}
        try:
            kitchens = Kitchen.objects.values('name', 'id').filter(store_id=store_id)

            response['status'] = True
            response['data'] = list(kitchens)

        except Exception as e:
            response['status'] = False
            response['msg'] = 'Some error occured ! Please reload the page'

        return JsonResponse(response)
