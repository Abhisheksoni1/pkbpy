from django.forms import model_to_dict
from django.shortcuts import render
from django.urls import reverse

from config import settings
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from pkbadmin.forms.promo_forms import PromoForm, PromoEditForm
from libraries.Functions import image_upload_handler, make_dir, join_string
from apps.common.models import PromoBanner, Store, Kitchen
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from libraries.DataTables import DataTables
import os
from django.contrib import messages
from pkbadmin.views.decorators import GroupRequiredMixin


class PromoBannersIndex(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'promos/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetPromoBanners(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        data = PromoBanner.objects.filter(is_deleted=False, status=True)
        datatable = DataTables(request, PromoBanner)
        datatable.COLUMN_SEARCH = ['title']
        datatable.select('id', 'title', 'description', 'image', 'status', 'kitchen_id', 'kitchen_id__name',
                         'kitchen__store__name')
        datatable.set_queryset(data)

        return datatable.response()


class AddPromoBanner(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = PromoForm
    initial = {"key": "value"}
    template_name = 'promos/create.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)

        if len(form['store']) == 0:
            messages.error(request, "Please create store first then add banner!", extra_tags="")
        return render(request, self.template_name, {'form': form, 'errors': form.errors})

    @staticmethod
    def directory_handler(promo_directory, promo_name):
        """ this function is written for images directory handling"""
        image_directory = make_dir(promo_directory + promo_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'])
        return image_directory

    def post(self, request):
        form = PromoForm(request.POST, request.FILES)
        current_user = request.user
        if form.is_valid():
            banner_name = join_string(form.cleaned_data['title'])
            print(form.cleaned_data['kitchen'])
            kitchen_obj = Kitchen.objects.get(id=int(form.cleaned_data['kitchen']))
            directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + join_string(
                kitchen_obj.store.name) + '/' +settings.CUSTOM_DIRS['KITCHEN_DIR']+join_string(kitchen_obj.name)
            promo_directory = make_dir(directory+'/'+ settings.CUSTOM_DIRS['BANNER_DIR'])
            directory_images = self.directory_handler(promo_directory, banner_name)
            # print(directory_images)
            """for database image directory path"""

            if request.FILES:
                img_path = image_upload_handler(request.FILES['banner'], directory_images
                                                )

                full_path = "{}".format(img_path)

                PromoBanner.objects.create(title=form.cleaned_data['title'],
                                           description=form.cleaned_data['description'],
                                           status=form.cleaned_data['status'],
                                           image=full_path,
                                           kitchen_id=int(form.cleaned_data['kitchen']),
                                           created_on=timezone.now(),
                                           created_by=current_user
                                           )
            return HttpResponseRedirect(reverse("custom-admin:promo_banner"))
        else:
            return render(request, self.template_name, {'form': form,
                                                        'errors': form.errors})


class UpdatePromoBanner(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = PromoEditForm
    initial = {"key": "value"}
    template_name = 'promos/edit.html'

    def get(self, request, pk):
        obj = PromoBanner.objects.get(pk=pk)
        obj.status = '1' if obj.status else '0'
        form = self.form_class(initial=model_to_dict(obj))
        image_path, banner_name, kitchen_name, store_name = obj.image, join_string(obj.title), join_string(
            obj.kitchen.name), join_string(obj.kitchen.store.name)

        image_path_split = image_path.split('/')
        image_path = image_path_split[-1]
        path = settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
               settings.CUSTOM_DIRS['KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
                   'BANNER_DIR'] + banner_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + image_path

        return render(request, self.template_name,
                      {'form': form, 'errors': form.errors, 'image_path': path, 'Store': obj.kitchen.store,
                       'Kitchen': obj.kitchen})

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            old_banner = join_string(PromoBanner.objects.get(id=pk).title)
            banner_name = join_string(form.cleaned_data['title'])
            obj = PromoBanner.objects.get(pk=pk)
            kitchen_obj = obj.kitchen
            store_name, kitchen_name = join_string(kitchen_obj.store.name), join_string(kitchen_obj.name)
            directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                        settings.CUSTOM_DIRS['KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
                            'BANNER_DIR']
            old_directory = directory + old_banner
            os.rename(old_directory, directory + banner_name)
            """for database image directory path"""
            directory_images = directory + banner_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR']
            if request.FILES.get('banner'):

                img_path = image_upload_handler(request.FILES['banner'], directory_images
                                                )

                full_path = "{}".format(img_path)
                PromoBanner.objects.filter(pk=pk).update(title=form.cleaned_data['title'],
                                                         description=form.cleaned_data['description'],
                                                         status=form.cleaned_data['status'],
                                                         image=full_path,
                                                         # kitchen_id=int(form.cleaned_data['kitchen']),
                                                         updated_on=timezone.now(), created_by=request.user)
            else:
                PromoBanner.objects.filter(pk=pk).update(title=form.cleaned_data['title'],
                                                         description=form.cleaned_data['description'],
                                                         status=form.cleaned_data['status'],
                                                         # kitchen_id=int(form.cleaned_data['kitchen']),
                                                         updated_on=timezone.now(), created_by=request.user)

            return HttpResponseRedirect(reverse("custom-admin:promo_banner"))

        return render(request, self.template_name, {'form': form, 'errors': form.errors})


class DeletePromoBanner(GroupRequiredMixin, APIView):
    group_required = ['Super admin']

    def get(self, request, pk):
        PromoBanner.objects.filter(pk=pk).update(is_deleted=True)
        return Response({"status": True, 'message': "promo-banner has been deleted successfully !"})
