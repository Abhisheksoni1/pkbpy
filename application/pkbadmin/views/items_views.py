from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import View
# from itertools import chain
from pkbadmin.views.decorators import GroupRequiredMixin
from apps.stores.models import Item, ItemPrice, Category, Kitchen
from config import settings
from libraries.DataTables import DataTables
from libraries.Functions import image_upload_handler, make_dir, join_string, file_upload_handler
from pkbadmin.forms.item_forms import ItemForm, UpdateItemForm
from pkbadmin.forms.import_csv_form import CsvImportForm
import os
import csv
from pkbadmin.forms.import_csv_form import CsvImportForm
from apps.users.models import User
import logging

class ItemsIndex(GroupRequiredMixin, View):
    group_required = ['Owner',"Manager"]

    template_name = 'items/index.html'
    form_class = CsvImportForm
    initial = {"key": "value"}

    def get(self, request):
        if "Owner" in request.user.group_name:
            store = request.user.storeowner.store.id
            form = self.form_class(self.initial,{'store':store})
        elif "Manager" in request.user.group_name:
            kitchen = request.user.kitchenmanager.kitchen.id
            store = request.user.kitchenmanager.kitchen.store.id
            form = self.form_class(self.initial, {'store':store,'kitchen': kitchen})

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


""" view for import csv data in item"""


class ImportCsvView(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager','Owner']

    def post(self, request):
        response = {'status': False, 'msg': '', 'data': {}}
        kitchen_id = request.POST.get('kitchen')
        kitchen = Kitchen.objects.get(id=kitchen_id)
        directory = make_dir(settings.MEDIA_ROOT + settings.CUSTOM_DIRS['CSV_DIR'])
        img_path = file_upload_handler(request.FILES.get('csv_file', None), directory)
        user = User.objects.get(id=1)
        csv_file = directory + img_path
        ItemModel = Item
        model_fields = [f.name for f in ItemModel._meta.fields]
        with open(csv_file, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            fields_name = next(reader)
            for i, _ in enumerate(fields_name):
                fields_name[i] = fields_name[i].lower()
                if not fields_name[i] == 'category_name':
                    if not fields_name[i] in model_fields:
                        response = {'status': False, 'msg': 'please give a required csv format', 'data': {}}
            try:
                for row in reader:
                    price_data = {}
                    base_price = 0.0
                    for i, field in enumerate(row):
                        if fields_name[i] == 'category_name':
                            category_name = field
                        if fields_name[i] == 'half':
                            if len(str(field)) > 0:
                                price_data[fields_name[i]] = field
                        if fields_name[i] == 'full':
                            if len(str(field)) > 0:
                                price_data[fields_name[i]] = field
                        if fields_name[i] == 'name':
                            name = field
                        if fields_name[i] == 'food_type':
                            food_type = field
                        if fields_name[i] == 'base_price':
                            if len(str(field)) > 0:
                                base_price = field
                    try:
                        category = Category.objects.get(kitchen_id=kitchen_id, name=category_name)
                        directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + \
                                    join_string(category.kitchen.store.name)+'/' + settings.CUSTOM_DIRS[
                                        'KITCHEN_DIR'] + join_string(category.kitchen.name)+'/'+settings.CUSTOM_DIRS[
                                        'CATEGORY_DIR']+join_string(category.name)


                    except Exception as e:
                        category = Category.objects.create(kitchen=kitchen, name=category_name,
                                                           created_by=user)
                        directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + \
                                    join_string(category.kitchen.store.name)+'/' + settings.CUSTOM_DIRS[
                                        'KITCHEN_DIR'] + join_string(category.kitchen.name)
                        directory = make_dir(directory+'/'+settings.CUSTOM_DIRS['CATEGORY_DIR']+join_string(category.name))
                        make_dir(directory+'/'+settings.CUSTOM_DIRS['IMAGE_DIR'])

                    item_obj = Item.objects.create(name=name, created_by=user, category=category,
                                                   food_type=food_type,
                                                   base_price=base_price)
                    make_dir(directory+'/'+settings.CUSTOM_DIRS['ITEM_DIR']+'/'+join_string(item_obj.name)+'/'+settings.CUSTOM_DIRS['IMAGE_DIR'])
                    item_obj.created_on = timezone.now()
                    item_obj.kitchen = category.kitchen
                    item_obj.store = category.kitchen.store
                    item_obj.save()


                    if len(price_data)>0:
                        for key, val in price_data.items():
                            try:
                                val = float(val)

                                ItemPrice.objects.create(
                                    quantity_type=key,
                                    price=val,
                                    item_id=item_obj.id,
                                    created_on=timezone.now(),
                                    created_by=user,
                                )
                                item_obj.is_variant = True
                                item_obj.save()
                            except Exception as e:
                                pass

                    response = {'status': True, 'msg': 'data has been uploaded for {} kitchen'.format(kitchen.name),
                                'data': {}}
            except Exception as e:
                print(e)
                response = {'status': False, 'msg': 'something went wrong please check category',
                            'data': {}}
        return JsonResponse(response)


class GetItems(GroupRequiredMixin, View):
    group_required = ['Manager','Owner']

    def post(self, request):
        if request.user.is_superuser:
            qs = Item.objects.filter(is_deleted=False)
            datatable = DataTables(request, Item)
            datatable.COLUMN_SEARCH = ['name', 'short_description', 'food_type']
            datatable.select('id', 'name', 'short_description', 'food_type', 'is_offer_active',
                             'is_outof_stock', 'category_id__name', 'base_price', 'status')
            datatable.set_queryset(qs)
            return datatable.response()
        elif 'Owner' in request.user.group_name:
            qs = Item.objects.filter(is_deleted=False,category__kitchen__store_id=request.user.storeowner.store.id)
            datatable = DataTables(request, Item)
            datatable.COLUMN_SEARCH = ['name', 'short_description', 'food_type']
            datatable.select('id', 'name', 'short_description', 'food_type', 'is_offer_active',
                             'is_outof_stock', 'category_id__name', 'base_price', 'status')
            datatable.set_queryset(qs)
            return datatable.response()
        elif 'Manager' in request.user.group_name:
            qs = Item.objects.filter(is_deleted=False, category__kitchen_id=request.user.kitchenmanager.kitchen.id)
            datatable = DataTables(request, Item)
            datatable.COLUMN_SEARCH = ['name', 'short_description', 'food_type']
            datatable.select('id', 'name', 'short_description', 'food_type', 'is_offer_active',
                             'is_outof_stock', 'category_id__name', 'base_price', 'status')
            datatable.set_queryset(qs)
            return datatable.response()




class AddItem(GroupRequiredMixin, View):
    group_required = ['Manager','Owner']

    form_class = ItemForm
    initial = {"key": "value"}
    template_name = 'items/create.html'

    def get(self, request):
        if "Owner" in request.user.group_name:
            store = request.user.storeowner.store.id
            form = self.form_class(self.initial, {'store': store})
        elif "Manager" in request.user.group_name:
            store = request.user.kitchenmanager.kitchen.store.id
            form = self.form_class(self.initial,{'store':store,'kitchen':request.user.kitchenmanager.kitchen.id})
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    @staticmethod
    def directory_handler(image_path, item_name):
        """ this function is written for images directory handling"""
        dir_name = make_dir(image_path + item_name + 'image/')

        return dir_name

    def post(self, request):
        if "Owner" in request.user.group_name:
            store = request.user.storeowner.store.id
        elif "Manager" in request.user.group_name:
            store = request.user.kitchenmanager.kitchen.store.id
        form = self.form_class(request.POST,{'store':store},request.FILES)
        if form.is_valid():

            item_name = form.cleaned_data['name']

            category_id_dir = int(form.cleaned_data['category_name'])
            category_obj = Category.objects.get(pk=category_id_dir)
            cat_name, kitchen_name, store_name = join_string(category_obj.name), join_string(
                category_obj.kitchen.name), join_string(category_obj.kitchen.store.name)

            directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
            img_path = os.path.join(directory, store_name,
                                    settings.CUSTOM_DIRS['KITCHEN_DIR'],
                                    kitchen_name,
                                    settings.CUSTOM_DIRS['CATEGORY_DIR'],
                                    cat_name,
                                    settings.CUSTOM_DIRS['ITEM_DIR']
                                    )

            # creating directory for this path
            item_name = join_string(item_name)
            dir_name = make_dir(img_path + item_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'])
            img_path = image_upload_handler(request.FILES.get('image', None), dir_name)

            item = Item.objects.create(name=form.cleaned_data['name'],
                                       description=form.cleaned_data['description'],
                                       short_description=form.cleaned_data['short_description'],
                                       category_id=int(form.cleaned_data['category_name']),
                                       image="{}".format(img_path) if img_path else "",
                                       image_thumb=("{}".format("T_" + img_path)) if img_path else "",
                                       food_type=form.cleaned_data['food_type'],
                                       is_offer_active=form.cleaned_data['is_offer_active'],
                                       is_outof_stock=form.cleaned_data['is_outof_stock'],
                                       base_price=form.cleaned_data['base_price'],
                                       is_variant=request.POST.get('is_variant') or False,
                                       created_on=timezone.now(),
                                       created_by=request.user,
                                       )

            price = request.POST.getlist('price')
            item_price_description = request.POST.getlist('item_price_description')

            quantity_types = request.POST.getlist('quantity_type')
            try:
                for i, quantity_type in enumerate(quantity_types):
                    ItemPrice.objects.create(
                        quantity_type=quantity_type,
                        price=price[i],
                        description=item_price_description[i],
                        item_id=item.id,
                        created_on=timezone.now(),
                        created_by=request.user,
                    )
            except Exception as e:
                print(e)
            return HttpResponseRedirect(reverse('custom-admin:items_index'))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class UpdateItem(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager','Owner']

    form_class = UpdateItemForm
    initial = {"key": "value"}
    template_name = 'items/edit.html'

    def get(self, request, pk):

        obj1 = Item.objects.get(pk=pk)
        form = self.form_class(model_to_dict(obj1))
        item_prices = obj1.itemprices.all()
        item_types = [item.quantity_type for item in item_prices]
        form.fields['is_outof_stock'].initial = obj1.is_outof_stock
        form.fields['is_offer_active'].initial = obj1.is_offer_active
        store = obj1.category.kitchen.store
        kitchen = obj1.category.kitchen
        category = obj1.category

        directory = settings.CUSTOM_DIRS['STORE_DIR'] + join_string(obj1.category.kitchen.store.name) + "/" + \
                    settings.CUSTOM_DIRS['KITCHEN_DIR'] + join_string(obj1.category.kitchen.name) \
                    + "/" + settings.CUSTOM_DIRS['CATEGORY_DIR'] + join_string(obj1.category.name) + "/" + \
                    settings.CUSTOM_DIRS['ITEM_DIR'] + join_string(obj1.name) + "/" + settings.CUSTOM_DIRS['IMAGE_DIR']

        return render(request, self.template_name, {'form': form,
                                                    'image_path': obj1.image,
                                                    'form_errors': form.errors,
                                                    'item_prices': item_prices,
                                                    'item_types': item_types,
                                                    'is_variant': obj1.is_variant,
                                                    'directory': directory,
                                                    'store': store,
                                                    'kitchen': kitchen,
                                                    'category': category
                                                    })

    @staticmethod
    def directory_handler(kitchen_directory, kitchen_name):
        """ this function is written for images directory handling"""
        make_dir(kitchen_directory)
        kitchen_directory = os.path.join(kitchen_directory, kitchen_name)
        make_dir(kitchen_directory)
        directory_images = os.path.join(kitchen_directory, 'images/')
        make_dir(directory_images)
        return directory_images

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        old_image = request.POST.get('old_image')
        item = Item.objects.get(pk=pk)
        store = item.category.kitchen.store
        kitchen = item.category.kitchen
        category = item.category
        if form.is_valid():
            item_name = form.cleaned_data['name']
            category_obj = item.category
            cat_name, kitchen_name, store_name = join_string(category_obj.name), join_string(
                category_obj.kitchen.name), join_string(category_obj.kitchen.store.name)

            directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']

            img_path = os.path.join(directory, store_name,
                                    settings.CUSTOM_DIRS['KITCHEN_DIR'],
                                    kitchen_name,
                                    settings.CUSTOM_DIRS['CATEGORY_DIR'],
                                    cat_name,
                                    settings.CUSTOM_DIRS['ITEM_DIR']
                                    )
            item_name = join_string(item_name)

            os.rename(img_path + join_string(category_obj.items.get(pk=pk).name), img_path + item_name)
            dir_name = os.path.join(img_path, item_name, settings.CUSTOM_DIRS['IMAGE_DIR'])
            img_path = image_upload_handler(request.FILES.get('image', None), dir_name)
            Item.objects.filter(pk=pk).update(name=form.cleaned_data['name'],
                                              description=form.cleaned_data['description'],
                                              short_description=form.cleaned_data['short_description'],
                                              image="{}".format(img_path) if img_path else old_image,
                                              image_thumb=(
                                                  "{}".format("T_" + img_path)) if img_path else "T_" + old_image,
                                              food_type=form.cleaned_data['food_type'],
                                              is_offer_active=form.cleaned_data['is_offer_active'],
                                              is_outof_stock=form.cleaned_data['is_outof_stock'],
                                              base_price=float(form.cleaned_data['base_price']),
                                              is_variant=True if request.POST.get("is_variant") else False,
                                              updated_on=timezone.now(),
                                              )

            item = Item.objects.get(pk=pk)

            price = request.POST.getlist('price')
            item_price_description = request.POST.getlist('item_price_description')
            quantity_type = request.POST.getlist('quantity_type')
            ItemPrice.objects.filter(item_id=item.id).delete()
            try:
                for i, quantity_type in enumerate(quantity_type):
                    ItemPrice.objects.create(
                        item_id=item.id,
                        quantity_type=quantity_type,
                        price=price[i],
                        description=item_price_description[i],
                        created_on=item.created_on,
                        updated_on=timezone.now()
                    )
            except Exception as e:
                print(e)

            return HttpResponseRedirect(reverse('custom-admin:items_index'))
        else:
            print(form.errors)
            return render(request, self.template_name,
                      {'form': form, 'form_errors': form.errors, 'store': store, 'kitchen': kitchen,
                       'category': category,'name':item.name})


class DeleteItems(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager','Owner']

    def get(self, request, pk):
        Item.objects.filter(pk=pk).update(is_deleted=True)
        return JsonResponse({"status": True, "message": "Item Successfully Deleted!"})


class GetStoreKitchens(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager','Owner']

    def post(self, request):
        store_id = request.POST.get('store_id')
        response = {}
        response = {'status': False, 'msg': '', 'data': {}}
        try:
            kitchens = Kitchen.objects.values('name', 'id').filter(store_id=store_id)

            response['status'] = True
            response['data'] = list(kitchens)
        except Exception as e:
            response['status'] = False
            response['msg'] = 'Some error occurred! Please reload the page.'

        return JsonResponse(response)


class GetKitchenCategory(GroupRequiredMixin, View):
    group_required =['Super admin', 'Manager','Owner']

    def post(self, request):
        kitchen_id = request.POST.get('kitchen_id')

        response = {'status': False, 'msg': '', 'data': {}}
        try:
            categories = Category.objects.values('name', 'id').filter(kitchen_id=kitchen_id,is_deleted = False)

            response['status'] = True
            response['data'] = list(categories)
        except Exception as e:
            response['status'] = False
            response['msg'] = 'Some error occurred ! Please reload the page.'

        return JsonResponse(response)


class DetailItem(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager','Owner']

    form_class = ItemForm
    initial = {"key": "value"}
    template_name = 'items/detail.html'

    def get(self, request, pk):
        obj = Item.objects.get(pk=pk)
        form = self.form_class(initial=model_to_dict(obj))
        return render(request, self.template_name, {'form': form,
                                                    'image_path': obj.image})
