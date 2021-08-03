import os
from django.shortcuts import render
from django.views import View

from libraries.Functions import make_dir, image_upload_handler
from pkbadmin.forms.promo_code_forms import PromoCodeForm,UpdatePromoCodeForm
from apps.discounts.models import PromoCode, PromoCodeAttribute
from pkbadmin.views.decorators import GroupRequiredMixin
from libraries.DataTables import DataTables
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
# from rest_framework.response import Response
from django.forms import model_to_dict
from config import settings
from libraries.Functions import join_string
from django.db import transaction


class PromoCodeIndex(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'promo_code/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetPromoCode(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):

        qs = PromoCode.objects.filter(is_deleted=False )
        # print(qs)
        datatable = DataTables(request, PromoCode)
        datatable.COLUMN_SEARCH = ['title']
        datatable.select('id', 'title', 'type', 'amount','percentage', 'max_discount', 'minimum_order', 'status')
        datatable.set_queryset(qs)


        return datatable.response()


class AddPromoCode(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = PromoCodeForm
    initial = {"key": "value"}
    template_name = 'promo_code/create.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors, }
                      )

    @staticmethod
    def directory_handler(image_path, promo_name):
        """ this function is written for images directory handling"""
        dir_name = make_dir(image_path + promo_name + '/')

        return dir_name

    def post(self, request):
        form = PromoCodeForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            title = join_string(title)
            labels = request.POST.getlist('labels')
            directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['PROMO_CODE_DIR']
            directory_images = self.directory_handler(directory, title)
            img_path = image_upload_handler(request.FILES.get('image', None),
                                            directory_images)
            print('todate',form.cleaned_data['to_date'])
            with transaction.atomic():
                code = PromoCode.objects.create(title=form.cleaned_data['title'],
                                                type=form.cleaned_data['type'],
                                                amount=form.cleaned_data['amount'],
                                                # discount_type=form.cleaned_data['type'],
                                                description=form.cleaned_data['description'],
                                                image=("{}".format(img_path)) if img_path else "",
                                                status=form.cleaned_data['status'],
                                                from_date=form.cleaned_data['from_date'],
                                                to_date=form.cleaned_data['to_date'],
                                                from_time=form.cleaned_data['from_time'],
                                                to_time=form.cleaned_data['to_time'],
                                                minimum_order=form.cleaned_data['minimum_order'],
                                                max_discount=form.cleaned_data.get('max_discount', None),
                                                percentage = form.cleaned_data.get('percentage',None),
                                                code=form.cleaned_data.get('code', None),
                                                created_on=timezone.now(),

                                                )
                for key in labels:
                    PromoCodeAttribute.objects.create(
                        key=key,
                        code_id=code.id,
                        created_by=request.user,
                        created_on=timezone.now()
                    )

            return HttpResponseRedirect(reverse('custom-admin:promo_code_index'))
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form,
                                                        'form_errors': form.errors})


class UpdatePromoCode(GroupRequiredMixin, View):
    group_required = ['Super admin']

    form_class = UpdatePromoCodeForm
    initial = {"key": "value"}
    template_name = 'promo_code/edit.html'

    @staticmethod
    def directory_handler(directory, name):
        image_directory = make_dir(directory + name + '/')
        return image_directory

    def get(self, request, pk):

        promocode = PromoCode.objects.get(id=pk)
        form = self.form_class(model_to_dict(promocode),initial={'pk': pk})
        promo_name = join_string(promocode.title)
        directory = settings.CUSTOM_DIRS['PROMO_CODE_DIR']
        directory_images = self.directory_handler(directory, promo_name)
        code_data = PromoCodeAttribute.objects.filter(
            code_id=pk
        )

        # print(directory_images)
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                                                    'directory_images': directory_images,
                                                    'image_path': promocode.image,
                                                    'old_name': promocode.title,'code_data':code_data})

    def post(self, request, pk):
        form = self.form_class(request.POST,initial={'pk': pk})
        old_image = request.POST.get('old_image')
        old_name = request.POST.get('old_name')
        labels = request.POST.getlist('labels')

        if form.is_valid():
            title = form.cleaned_data['title']
            title = join_string(title)
            directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['PROMO_CODE_DIR']

            os.rename(directory + join_string(old_name), directory + title)
            directory_images = directory + title + '/'
            # print(directory_images)
            img_path = image_upload_handler(request.FILES.get('image', None),
                                            directory_images)
            PromoCode.objects.filter(pk=pk).update(title=form.cleaned_data['title'],
                                                   type=form.cleaned_data['type'],
                                                   # discount_type=form.cleaned_data['type'],
                                                   description=form.cleaned_data['description'],
                                                   image=("{}".format(img_path)) if img_path else old_image,
                                                   status=form.cleaned_data['status'],
                                                   from_date=form.cleaned_data['from_date'],
                                                   to_date=form.cleaned_data['to_date'],
                                                   from_time=form.cleaned_data['from_time'],
                                                   to_time=form.cleaned_data['to_time'],
                                                   minimum_order=form.cleaned_data['minimum_order'],
                                                   max_discount=form.cleaned_data.get('max_discount', None),
                                                   code=form.cleaned_data.get('code', None),
                                                   percentage=form.cleaned_data.get('percentage', None),
                                                   created_on=timezone.now(),

                                                   )
            for key in labels:
                PromoCodeAttribute.objects.create(
                    key=key,
                    code_id=pk,
                    created_by=request.user,
                    created_on=timezone.now()
                )

            return HttpResponseRedirect(reverse('custom-admin:promo_code_index'))
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form,
                                                        'form_errors': form.errors})


class DeletePromoCode(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def get(self, request, pk):
        offer = PromoCode.objects.filter(pk=pk).update(is_deleted=True)
        print(offer)
        return JsonResponse({"status": True, 'message': "Promo Code Successfully Deleted!"})
