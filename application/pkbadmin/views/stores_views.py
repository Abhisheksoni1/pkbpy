# from django.contrib.gis.geos import Point
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from config import settings
from pkbadmin.forms.store_forms import StoreForm
from apps.stores.models import Store, StoreManager, StoreOwner, StoreAttribute
from django.http import HttpResponseRedirect, JsonResponse
from libraries.Functions import image_upload_handler, make_dir, join_string
from django.db import transaction
from libraries.DataTables import DataTables
from django.forms.models import model_to_dict
from pkbadmin.views.decorators import GroupRequiredMixin


# import os

class StoresIndex(GroupRequiredMixin, View):
    group_required = ['Super admin','Owner']
    template_name = 'stores/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetStores(GroupRequiredMixin, View):
    group_required = ['Super admin','Owner']

    def post(self, request):
        user = request.user
        if user.is_superuser:
            qs = Store.objects.filter(is_deleted=False)
        else:
            qs = Store.objects.filter(is_deleted=False, manager__manager=user)

        datatable = DataTables(request, Store)
        datatable.COLUMN_SEARCH = ['name', 'tag_line', 'description', 'address']
        datatable.select('id', 'name', 'tag_line', 'description', 'address', 'status')
        datatable.set_queryset(qs)

        return datatable.response()


class AddStore(GroupRequiredMixin, View):
    group_required = ['Owner']

    form_class = StoreForm
    initial = {"key": "value"}
    template_name = 'stores/create.html'

    def get(self, request):
        form = self.form_class(initial=self.initial, user=request.user)
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    @staticmethod
    def directory_handler(directory, store_name):
        """created image and logo directory path static method used since need again same directory in Update class"""
        image_directory = make_dir(directory + store_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'])
        logo_directory = make_dir(directory + store_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'])
        return image_directory, logo_directory

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, user=request.user)
        labels = request.POST.getlist('labels')
        values = request.POST.getlist('value')
        dictionary = dict(zip(labels, values))

        if form.is_valid():
            directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
            store_name = form.cleaned_data['name']
            store_name = join_string(store_name)

            directory_images, directory_logo = self.directory_handler(directory, store_name)

            img_path = image_upload_handler(request.FILES.get('image', None),
                                            directory_images)
            logo_path = image_upload_handler(request.FILES.get('logo', None),
                                             directory_logo)

            # manager = int(form.cleaned_data['manager'])

            with transaction.atomic():
                try:
                    store = Store.objects.create(name=form.cleaned_data['name'],
                                                 tag_line=form.cleaned_data['tag_line'],
                                                 logo=("{}".format(logo_path)) if logo_path else "",
                                                 logo_thumb=("{}".format("T_" + logo_path)) if logo_path else "",
                                                 description=form.cleaned_data['description'],
                                                 location=form.cleaned_data['location'],
                                                 address=form.cleaned_data['address'],
                                                 tin_no=form.cleaned_data['tin_no'],
                                                 image=("{}".format(img_path)) if img_path else "",
                                                 image_thumb=("{}".format("T_" + img_path)) if img_path else "",
                                                 opening_time=form.cleaned_data['opening_time'],
                                                 closing_time=form.cleaned_data['closing_time'],
                                                 delivery_time=form.cleaned_data['delivery_time'],
                                                 cost_for_two=form.cleaned_data['cost_for_two'],
                                                 minimum_order=form.cleaned_data['minimum_order'],
                                                 created_on=timezone.now(),
                                                 created_by=request.user,

                                                 )

                    # for key, value in dictionary.items():
                    #     StoreAttribute.objects.create(
                    #         key=key,
                    #         value=value,
                    #         store_id=store.id,
                    #         created_by=request.user,
                    #         created_on=timezone.now()
                    #     )

                    StoreOwner.objects.create(store_id=store.id, owner_id=request.user.id)
                    # StoreManager.objects.create(store_id=store.id, manager_id=manager)

                    return HttpResponseRedirect(reverse("custom-admin:index"))
                except Exception as e:
                    print(e)
                    print(form.errors)
                    return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                                                                })

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class UpdateStore(GroupRequiredMixin, View):
    group_required = ['Owner']

    form_class = StoreForm
    initial = {"key": "value"}
    template_name = 'stores/edit.html'

    @staticmethod
    def directory_handler(directory, store_name):
        """created image and logo directory path static method used since need again same directory in Update class"""
        image_directory = make_dir(directory + store_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'])
        logo_directory = make_dir(directory + store_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'])
        return image_directory, logo_directory

    def get(self, request, pk):
        store = Store.objects.get(pk=pk)
        # manager = StoreManager.objects.get(store_id=store.id)
        # store_attributes = list(store.attributes.values('key', 'value'))
        form = self.form_class(initial=model_to_dict(store), user=request.user)
        directory = settings.CUSTOM_DIRS['STORE_DIR']
        store_name = join_string(store.name)
        directory_images = os.path.join(directory,store_name,settings.CUSTOM_DIRS['IMAGE_DIR'])
        directory_logo = os.path.join(directory,store_name,settings.CUSTOM_DIRS['LOGO_DIR'])
        # form.fields['manager'].initial = manager.manager_id
        if store.location is not None:
            form.fields['longitude'].initial, form.fields['latitude'].initial = store.location[0], store.location[1]

        return render(request, self.template_name, {'form': form, 'logo_path': store.logo,
                                                    'image_path': store.image,
                                                    'form_errors': form.errors,
                                                    'directory_logo': directory_logo,
                                                    'directory_image': directory_images,
                                                    'old_name': store.name,
                                                    })

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES, user=request.user)
        old_image = request.POST.get('old_image')
        old_logo = request.POST.get('old_logo')
        old_name = request.POST.get('old_name')

        if form.is_valid():
            directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
            store_name = form.cleaned_data['name']
            store_name = join_string(store_name)
            os.rename(directory+join_string(old_name), directory+store_name)
            image_directory = directory + store_name + "/" + settings.CUSTOM_DIRS['IMAGE_DIR']
            logo_directory = directory + store_name + "/" + settings.CUSTOM_DIRS['LOGO_DIR']
            img_path = image_upload_handler(request.FILES.get('image', None), image_directory)
            logo_path = image_upload_handler(request.FILES.get('logo', None),
                                             logo_directory)

            # manager = int(form.cleaned_data['manager'])
            with transaction.atomic():
                try:

                    Store.objects.filter(pk=pk).update(
                        name=form.cleaned_data['name'],
                        tag_line=form.cleaned_data['tag_line'],
                        logo=("{}".format(logo_path)) if logo_path else old_logo,
                        logo_thumb=("{}".format("T_" + logo_path)) if logo_path else "T_"+old_logo ,
                        description=form.cleaned_data['description'],
                        location=form.cleaned_data['location'],
                        address=form.cleaned_data['address'],
                        tin_no=form.cleaned_data['tin_no'],
                        image=("{}".format(img_path)) if img_path else old_image,
                        image_thumb=("{}".format("T_" + img_path)) if img_path else "T_"+old_image,
                        opening_time=form.cleaned_data['opening_time'],
                        closing_time=form.cleaned_data['closing_time'],
                        delivery_time=form.cleaned_data['delivery_time'],
                        cost_for_two=form.cleaned_data['cost_for_two'],
                        minimum_order=form.cleaned_data['minimum_order'],

                        updated_on=timezone.now()
                    )

                    # store = Store.objects.get(pk=pk)
                    # StoreAttribute.objects.filter(store_id=store.id).delete()
                    # for key, value in dictionary.items():
                    #     StoreAttribute.objects.create(
                    #         key=key,
                    #         value=value,
                    #         store_id=store.id,
                    #         created_by=request.user,
                    #         created_on=timezone.now()
                    #     )
                    # StoreOwner.objects.filter(store_id=store.id).update(owner_id=store.created_by_id)
                    # StoreManager.objects.filter(store_id=store.id).update(manager_id=manager)

                    return HttpResponseRedirect(reverse("custom-admin:index"))
                except Exception as e:
                    return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                                                                "error": "This manager has been already assigned a store."})

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class DetailStore(GroupRequiredMixin, View):
    group_required = ['Owner']

    form_class = StoreForm
    initial = {"key": "value"}
    template_name = 'stores/detail.html'

    def get(self, request, pk):
        obj = Store.objects.get(pk=pk)
        form = self.form_class(initial=model_to_dict(obj))
        return render(request, self.template_name, {'form': form, 'logo_path': obj.logo,
                                                    'image_path': obj.image})


class DeleteStores(GroupRequiredMixin, View):
    group_required = ['Owner']

    def get(self, request, pk):
        Store.objects.filter(pk=pk).update(is_deleted=True)
        return JsonResponse({"status": True, "message": "Store deleted successfully!"})
