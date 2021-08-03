from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.utils import timezone
from config import settings
from libraries.Functions import image_upload_handler, make_dir, join_string
from pkbadmin.forms.kitchen_forms import KitchenForm, UpdateKitchenForm
from apps.stores.models import Kitchen, KitchenAttribute,KitchenManager
from libraries.DataTables import DataTables
from apps.stores.models import Store,StoreOwner
import os
from django.db import transaction
from django.forms.models import model_to_dict
from pkbadmin.views.decorators import GroupRequiredMixin
import uuid
from django.db.models import Q
from django.contrib import messages
from apps.users.models import User, Group
class KitchensIndex(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner','Manager']
    template_name = 'kitchens/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetKitchens(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Owner','Manager']

    def post(self, request):
        if request.user.is_superuser:
            qs = Kitchen.objects.filter(is_deleted=False)

            datatable = DataTables(request, Kitchen)
            datatable.COLUMN_SEARCH = ['name', 'tag_line', 'description', 'address']
            datatable.select('id', 'name', 'tag_line', 'description', 'address', 'store_id__name',
                             'status', 'short_name')
            datatable.set_queryset(qs)
            return datatable.response()
        else:
            try:
                store = StoreOwner.objects.get(owner=request.user)
                qs = Kitchen.objects.filter(is_deleted=False,store_id=store.store.id)
                datatable = DataTables(request, Kitchen)
                datatable.COLUMN_SEARCH = ['name', 'tag_line', 'description', 'address']
                datatable.select('id', 'name', 'tag_line', 'description', 'address', 'store_id__name',
                                 'status', 'short_name')
                datatable.set_queryset(qs)

                return datatable.response()
            except:
                messages.error(request, "Please add Store first.", extra_tags="")
                return HttpResponseRedirect(reverse("custom-admin:index"))


class AddKitchen(GroupRequiredMixin, View):
    group_required = ['Owner']
    form_class = KitchenForm
    initial = {"key": "value"}
    template_name = 'kitchens/create.html'

    def get(self, request):
        store = self.request.user.storeowner.store.id
        form = self.form_class(self.initial,{'store': store})
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    @staticmethod
    def directory_handler(kitchen_directory, kitchen_name):
        """to create image and logo directory wrote static because need to use in Update method as wel"""
        images_directory = make_dir(kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'])
        logo_directory = make_dir(kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'])

        return images_directory, logo_directory

    def post(self, request):
        store = self.request.user.storeowner.store.id
        form = self.form_class(request.POST, {'store': store},request.FILES)
        # labels = request.POST.getlist('labels')
        # values = request.POST.getlist('value')
        # dictionary = dict(zip(labels, values))

        if form.is_valid():

            store_id = int(form.cleaned_data['store'])

            kitchens = Kitchen.objects.filter(store_id=store_id).values_list('name', flat=True)

            name = form.cleaned_data['name']

            if name not in kitchens:

                store_obj = Store.objects.get(pk=store_id)
                store_name, kitchen_name = store_obj.name, form.cleaned_data['name']
                store_name, kitchen_name = join_string(store_name), join_string(kitchen_name)
                directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
                kitchen_directory = os.path.join(directory, store_name, settings.CUSTOM_DIRS['KITCHEN_DIR'])

                images_directory, logo_directory = self.directory_handler(kitchen_directory, kitchen_name)

                img_path = image_upload_handler(request.FILES.get('image', None), images_directory
                                                )

                logo_path = image_upload_handler(request.FILES.get('logo', None),
                                                 logo_directory)
                with transaction.atomic():
                    kitchen = Kitchen.objects.create(name=form.cleaned_data['name'],
                                                     tag_line=form.cleaned_data['tag_line'],
                                                     logo=("{}".format(logo_path)) if logo_path else "",
                                                     logo_thumb=("{}".format("T_" + logo_path)) if logo_path else "",
                                                     description=form.cleaned_data['description'],
                                                     location=form.cleaned_data['location'],
                                                     address=form.cleaned_data['address'],
                                                     image=("{}".format(img_path)) if img_path else "",
                                                     image_thumb=("{}".format("T_" + img_path)) if img_path else "",
                                                     store_id=int(form.cleaned_data['store']),
                                                     delivery_time=form.cleaned_data['delivery_time'],
                                                     cost_for_two=form.cleaned_data['cost_for_two'],
                                                     minimum_order=form.cleaned_data['minimum_order'],
                                                     opening_time=form.cleaned_data['opening_time'],
                                                     closing_time=form.cleaned_data['closing_time'],
                                                     mobile=form.cleaned_data['mobile'],
                                                     delivery_charges=form.cleaned_data['delivery_charges'],
                                                     packing_charges=form.cleaned_data['packing_charges'],
                                                     created_on=timezone.now(),
                                                     created_by=request.user,
                                                     short_name=form.cleaned_data['short_name'],
                                                     cod_limit=(
                                                         float(form.cleaned_data['cod_limit']) if form.cleaned_data[
                                                             'cod_limit'] else None),
                                                     )

                    # for key, value in dictionary.items():
                    #     KitchenAttribute.objects.create(
                    #         key=key,
                    #         value=value,
                    #         kitchen_id=kitchen.id,
                    #         created_by=request.user,
                    #         created_on=timezone.now()
                    #     )

                    return HttpResponseRedirect(reverse('custom-admin:kitchens_index'))
            else:
                name_error = "This name is already taken for this store."
                return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                                                            'name_error': name_error})

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class UpdateKitchen(GroupRequiredMixin, View):
    group_required = ['Manager', 'Owner']

    form_class = UpdateKitchenForm
    initial = {"key": "value"}
    template_name = 'kitchens/edit.html'

    @staticmethod
    def directory_handler(kitchen_directory, kitchen_name):
        """to create image and logo directory wrote static because need to use in Update method as wel"""
        images_directory = make_dir(kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'])
        logo_directory = make_dir(kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'])

        return images_directory, logo_directory

    def get(self, request, pk):
        obj = Kitchen.objects.get(pk=pk)
        # kitchen_attributes = list(obj.attributes.values('key', 'value'))
        form = self.form_class(initial=model_to_dict(obj))
        directory = settings.CUSTOM_DIRS['STORE_DIR'] + join_string(obj.store.name) + "/" + settings.CUSTOM_DIRS[
            'KITCHEN_DIR']
        kitchen_name = join_string(obj.name)
        directory_images, directory_logo = self.directory_handler(directory, kitchen_name)

        if obj.location is not None:
            form.fields['longitude'].initial, form.fields['latitude'].initial = obj.location[0], obj.location[1]
        store = obj.store
        return render(request,
                      self.template_name,
                      {
                          'form': form,
                          'logo_path': obj.logo,
                          'image_path': obj.image,
                          'form_errors': form.errors,
                          'directory_logo': directory_logo,
                          'directory_image': directory_images,
                          'old_name': obj.name,
                          'store': store
                      })

    def post(self, request, pk):
        if 'Owner' in request.user.group_name :
            form = self.form_class(request.POST, request.FILES)
            # labels = request.POST.getlist('labels')
            # values = request.POST.getlist('value')
            # dictionary = dict(zip(labels, values))
            old_image = request.POST.get('old_image')
            old_logo = request.POST.get('old_logo')
            old_name = request.POST.get('old_name')
            kitchen = Kitchen.objects.get(pk=pk)
            store_id = kitchen.store.id
            store_ob = Store.objects.get(pk=store_id)
            # print(store_id)
            if form.is_valid():
                kitchens = Kitchen.objects.filter(~Q(id=pk), store_id=store_id).values_list('name', flat=True)
                name = form.cleaned_data['name']
                print(kitchens)

                if name  not in kitchens:
                    store_obj = Store.objects.get(pk=store_id)
                    store_name = join_string(store_obj.name)
                    directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
                    kitchen_directory = os.path.join(directory, store_name, settings.CUSTOM_DIRS['KITCHEN_DIR'])
                    os.rename(kitchen_directory + join_string(store_obj.kitchens.get(pk=pk).name),
                              kitchen_directory + join_string(form.cleaned_data['name']))
                    kitchen_name = join_string(form.cleaned_data['name'])
                    images_directory = kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR']
                    logo_directory = kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR']
                    img_path = image_upload_handler(request.FILES.get('image', None), images_directory
                                                    )

                    logo_path = image_upload_handler(request.FILES.get('logo', None),
                                                     logo_directory)
                    with transaction.atomic():
                        kitchen = Kitchen.objects.get(id=pk)
                        Kitchen.objects.filter(pk=pk).update(
                            name=form.cleaned_data['name'],
                            tag_line=form.cleaned_data['tag_line'],
                            logo=("{}".format(logo_path)) if logo_path else old_logo,
                            logo_thumb=("{}".format("T_" + logo_path)) if logo_path else "T_" + old_logo,
                            description=form.cleaned_data['description'],
                            location=form.cleaned_data['location'],
                            address=form.cleaned_data['address'],
                            image=("{}".format(img_path)) if img_path else old_image,
                            image_thumb=("{}".format("T_" + img_path)) if img_path else "T_" + old_image,
                            delivery_time=form.cleaned_data['delivery_time'],
                            cost_for_two=form.cleaned_data['cost_for_two'],
                            minimum_order=form.cleaned_data['minimum_order'],
                            opening_time=form.cleaned_data['opening_time'],
                            closing_time=form.cleaned_data['closing_time'],
                            mobile=form.cleaned_data['mobile'],
                            delivery_charges=form.cleaned_data['delivery_charges'],
                            packing_charges=form.cleaned_data['packing_charges'],
                            short_name=form.cleaned_data['short_name'],
                            cod_limit=(float(form.cleaned_data['cod_limit']) if form.cleaned_data['cod_limit'] else None),
                            updated_on=timezone.now(),
                        )

                        # kitchen = Kitchen.objects.get(pk=pk)
                        # KitchenAttribute.objects.filter(kitchen_id=kitchen.id).delete()
                        # for key, value in dictionary.items():
                        #     KitchenAttribute.objects.create(
                        #         key=key,
                        #         value=value,
                        #         kitchen_id=kitchen.id,
                        #         created_by=request.user,
                        #         created_on=timezone.now()
                        #     )

                        return HttpResponseRedirect(reverse('custom-admin:kitchens_index'))

                # elif name in kitchens and name == old_name:
                #     store_obj = Store.objects.get(pk=store_id)
                #     store_name = join_string(store_obj.name)
                #     directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
                #     kitchen_directory = os.path.join(directory, store_name, settings.CUSTOM_DIRS['KITCHEN_DIR'])
                #     os.rename(kitchen_directory + join_string(store_obj.kitchens.get(pk=pk).name),
                #               kitchen_directory + join_string(form.cleaned_data['name']))
                #     kitchen_name = join_string(form.cleaned_data['name'])
                #     images_directory = kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR']
                #     logo_directory = kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR']
                #     img_path = image_upload_handler(request.FILES.get('image', None), images_directory
                #                                     )
                #
                #     logo_path = image_upload_handler(request.FILES.get('logo', None),
                #                                      logo_directory)
                #
                #     with transaction.atomic():
                #         Kitchen.objects.filter(pk=pk).update(
                #             name=old_name,
                #             tag_line=form.cleaned_data['tag_line'],
                #             logo=("{}".format(logo_path)) if logo_path else old_logo,
                #             description=form.cleaned_data['description'],
                #             location=form.cleaned_data['location'],
                #             address=form.cleaned_data['address'],
                #             image=("{}".format(img_path)) if img_path else old_image,
                #             image_thumb=("{}".format("T_" + img_path)) if img_path else old_image,
                #             delivery_time=form.cleaned_data['delivery_time'],
                #             cost_for_two=form.cleaned_data['cost_for_two'],
                #             minimum_order=form.cleaned_data['minimum_order'],
                #             opening_time=form.cleaned_data['opening_time'],
                #             closing_time=form.cleaned_data['closing_time'],
                #             mobile=form.cleaned_data['mobile'],
                #             delivery_charges=form.cleaned_data['delivery_charges'],
                #             packing_charges=form.cleaned_data['packing_charges'],
                #             short_name=form.cleaned_data['short_name'],
                #             cod_limit=(float(form.cleaned_data['cod_limit']) if form.cleaned_data['cod_limit'] else None),
                #             updated_on=timezone.now(),
                #         )
                #
                #         # kitchen = Kitchen.objects.get(pk=pk)
                #         # KitchenAttribute.objects.filter(kitchen_id=kitchen.id).delete()
                #         # for key, value in dictionary.items():
                #         #     KitchenAttribute.objects.create(
                #         #         key=key,
                #         #         value=value,
                #         #         kitchen_id=kitchen.id,
                #         #         created_by=request.user,
                #         #         created_on=timezone.now()
                #         #     )
                #
                #         return HttpResponseRedirect(reverse('custom-admin:kitchens_index'))

                else:
                    name_error = "This name has been taken already."
                    print(form.errors)
                    return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                                                            'name_error': name_error,'store':store_ob})

            else:
                print(form.errors)
                return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                                                           'store': store_ob})
        else:

            form = self.form_class(request.POST, request.FILES)
            # labels = request.POST.getlist('labels')
            # values = request.POST.getlist('value')
            # dictionary = dict(zip(labels, values))
            old_image = request.POST.get('old_image')
            old_logo = request.POST.get('old_logo')
            old_name = request.POST.get('old_name')
            kitchen = Kitchen.objects.get(pk=pk)
            store_id = kitchen.store.id
            store_ob = Store.objects.get(pk=store_id)
            # print(store_id)
            if form.is_valid():
                kitchens = Kitchen.objects.filter(~Q(id=pk), store_id=store_id).values_list('name', flat=True)
                name = form.cleaned_data['name']

                if name not in kitchens:
                    store_obj = Store.objects.get(pk=store_id)
                    store_name = join_string(store_obj.name)
                    directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
                    kitchen_directory = os.path.join(directory, store_name, settings.CUSTOM_DIRS['KITCHEN_DIR'])
                    os.rename(kitchen_directory + join_string(store_obj.kitchens.get(pk=pk).name),
                              kitchen_directory + join_string(form.cleaned_data['name']))
                    kitchen_name = join_string(form.cleaned_data['name'])
                    images_directory = kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR']
                    logo_directory = kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR']
                    img_path = image_upload_handler(request.FILES.get('image', None), images_directory
                                                    )

                    logo_path = image_upload_handler(request.FILES.get('logo', None),
                                                     logo_directory)
                    with transaction.atomic():
                        kitchen = Kitchen.objects.get(id=pk)
                        Kitchen.objects.filter(pk=pk).update(
                            name=form.cleaned_data['name'],
                            tag_line=form.cleaned_data['tag_line'],
                            logo=("{}".format(logo_path)) if logo_path else old_logo,
                            logo_thumb=("{}".format("T_" + logo_path)) if logo_path else "T_" + old_logo,
                            description=form.cleaned_data['description'],
                            location=form.cleaned_data['location'],
                            address=form.cleaned_data['address'],
                            image=("{}".format(img_path)) if img_path else old_image,
                            image_thumb=("{}".format("T_" + img_path)) if img_path else "T_" + old_image,
                            delivery_time=form.cleaned_data['delivery_time'],
                            cost_for_two=form.cleaned_data['cost_for_two'],
                            minimum_order=form.cleaned_data['minimum_order'],
                            opening_time=form.cleaned_data['opening_time'],
                            closing_time=form.cleaned_data['closing_time'],
                            mobile=form.cleaned_data['mobile'],
                            delivery_charges=form.cleaned_data['delivery_charges'],
                            packing_charges=form.cleaned_data['packing_charges'],
                            short_name=form.cleaned_data['short_name'],
                            cod_limit=(
                                float(form.cleaned_data['cod_limit']) if form.cleaned_data['cod_limit'] else None),
                            updated_on=timezone.now(),
                        )

                        # kitchen = Kitchen.objects.get(pk=pk)
                        # KitchenAttribute.objects.filter(kitchen_id=kitchen.id).delete()
                        # for key, value in dictionary.items():
                        #     KitchenAttribute.objects.create(
                        #         key=key,
                        #         value=value,
                        #         kitchen_id=kitchen.id,
                        #         created_by=request.user,
                        #         created_on=timezone.now()
                        #     )

                        return HttpResponseRedirect(reverse('custom-admin:index'))

                # elif name in kitchens and name == old_name:
                #     store_obj = Store.objects.get(pk=store_id)
                #     store_name = join_string(store_obj.name)
                #     directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR']
                #     kitchen_directory = os.path.join(directory, store_name, settings.CUSTOM_DIRS['KITCHEN_DIR'])
                #     os.rename(kitchen_directory + join_string(store_obj.kitchens.get(pk=pk).name),
                #               kitchen_directory + join_string(form.cleaned_data['name']))
                #     kitchen_name = join_string(form.cleaned_data['name'])
                #     images_directory = kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR']
                #     logo_directory = kitchen_directory + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR']
                #     img_path = image_upload_handler(request.FILES.get('image', None), images_directory
                #                                     )
                #
                #     logo_path = image_upload_handler(request.FILES.get('logo', None),
                #                                      logo_directory)
                #
                #     with transaction.atomic():
                #         Kitchen.objects.filter(pk=pk).update(
                #             name=old_name,
                #             tag_line=form.cleaned_data['tag_line'],
                #             logo=("{}".format(logo_path)) if logo_path else old_logo,
                #             description=form.cleaned_data['description'],
                #             location=form.cleaned_data['location'],
                #             address=form.cleaned_data['address'],
                #             image=("{}".format(img_path)) if img_path else old_image,
                #             image_thumb=("{}".format("T_" + img_path)) if img_path else old_image,
                #             delivery_time=form.cleaned_data['delivery_time'],
                #             cost_for_two=form.cleaned_data['cost_for_two'],
                #             minimum_order=form.cleaned_data['minimum_order'],
                #             opening_time=form.cleaned_data['opening_time'],
                #             closing_time=form.cleaned_data['closing_time'],
                #             mobile=form.cleaned_data['mobile'],
                #             delivery_charges=form.cleaned_data['delivery_charges'],
                #             packing_charges=form.cleaned_data['packing_charges'],
                #             short_name=form.cleaned_data['short_name'],
                #             cod_limit=(
                #                 float(form.cleaned_data['cod_limit']) if form.cleaned_data['cod_limit'] else None),
                #             updated_on=timezone.now(),
                #         )

                        # kitchen = Kitchen.objects.get(pk=pk)
                        # KitchenAttribute.objects.filter(kitchen_id=kitchen.id).delete()
                        # for key, value in dictionary.items():
                        #     KitchenAttribute.objects.create(
                        #         key=key,
                        #         value=value,
                        #         kitchen_id=kitchen.id,
                        #         created_by=request.user,
                        #         created_on=timezone.now()
                        #     )

                        # return HttpResponseRedirect(reverse('custom-admin:index'))

            else:
                name_error = "This name has been taken already."
                return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                                                    'name_error': name_error,'store':store_ob})
        print(form.errors)
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors, 'store': store_ob})


class DeleteKitchen(GroupRequiredMixin, View):
    group_required = ['Manager', 'Owner']

    def get(self, request, pk):
        Kitchen.objects.filter(pk=pk).update(is_deleted=True)
        try:
            kitchen_manager=KitchenManager.objects.get(kitchen_id=pk)
            user = kitchen_manager.manager
            user = User.objects.get(mobile=user)
            user.is_active = False
            user.save()
            KitchenManager.objects.filter(manager_id=pk).delete()
        except Exception as e:
            pass

        return JsonResponse({"status": True, "message": "Kitchen deleted successfully!"})


class DetailKitchen(GroupRequiredMixin, View):
    group_required = ['Manager', 'Owner']

    form_class = KitchenForm
    initial = {"key": "value"}
    template_name = 'kitchens/detail.html'

    def get(self, request, pk):
        obj = Kitchen.objects.get(pk=pk)
        form = self.form_class(initial=model_to_dict(obj))
        if obj.location is not None:
            form.fields['longitude'].initial, form.fields['latitude'].initial = obj.location[0], obj.location[1]
        return render(request, self.template_name, {'form': form, 'logo_path': obj.logo,
                                                    'image_path': obj.image})
