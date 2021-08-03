from django.forms import model_to_dict
from django.urls import reverse
from rest_framework.views import APIView
from django.shortcuts import render
from pkbadmin.serializers.store_serializer import StoreSerializer
from libraries.DataTables import DataTables
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from pkbadmin.forms.discount_form import DiscountForm
from apps.discounts.models import Discount, DiscountOnItem
from apps.stores.models import Store
from pkbadmin.views.decorators import GroupRequiredMixin
from django.db import transaction

class DiscountsIndex(GroupRequiredMixin, View):
    group_required = ['Super admin','Owner']
    template_name = 'discounts/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetDiscounts(GroupRequiredMixin, View):
    group_required = ['Super admin','Owner']

    def post(self, request):
        qs = Discount.objects.filter(is_deleted=False,created_by=request.user)
        print(qs)
        # print(qs)
        datatable = DataTables(request, Discount)
        datatable.COLUMN_SEARCH = ['title']
        datatable.select('id', 'title', 'type', 'amount', 'order_type', 'validate_on_code', 'percentage', 'status',
                         'add_on')
        datatable.set_queryset(qs)

        return datatable.response()


class AddDiscount(GroupRequiredMixin, View):
    group_required =['Owner']
    form_class = DiscountForm
    initial = {"key": "value"}
    template_name = 'discounts/create.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        store_id = request.user.storeowner.store.id
        store = Store.objects.filter(id=store_id)
        try:
            store_serializer = StoreSerializer(store, many=True)
            data = store_serializer.data

            return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                                                        'data': data})
        except Exception as e:
            return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    def post(self, request):
        form = DiscountForm(request.POST, request.FILES)
        order_type = request.POST.getlist('order_type')
        item_list = request.POST.getlist('item_id')
        time_range = request.POST.get('datetimes')
        if form.is_valid():
            with transaction.atomic():
                discount = Discount.objects.create(title=form.cleaned_data['title'],
                                                   type=form.cleaned_data['type'],
                                                   # discount_type=form.cleaned_data['type'],
                                                   description=form.cleaned_data['description'],
                                                   terms_and_conditions=form.cleaned_data['terms_and_conditions'],
                                                   order_type=",".join(i for i in order_type),
                                                   validate_on_code=form.cleaned_data['validate_on_code'],
                                                   status=form.cleaned_data['status'],
                                                   from_date=form.cleaned_data['from_date'],
                                                   to_date=form.cleaned_data['to_date'],
                                                   amount=form.cleaned_data['amount'],
                                                   from_time=form.cleaned_data['from_time'],
                                                   to_time=form.cleaned_data['to_time'],
                                                   code=form.cleaned_data['code'],
                                                   add_on=form.cleaned_data['add_on'],
                                                   # amount = form.cleaned_data['percentage'],
                                                   percentage=form.cleaned_data.get('percentage',None),
                                                   created_on=timezone.now(),
                                                   created_by=request.user

                                                   )
                """ discount applied on item when store is selected"""
                if item_list:

                    for i in item_list:
                        DiscountOnItem.objects.create(
                            discount_id=discount.id,
                            item_id=i
                        )

            return HttpResponseRedirect(reverse('custom-admin:discount_index'))
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form,
                                                        'form_errors': form.errors})


class UpdateDiscount(GroupRequiredMixin, View):
    group_required = ['Super admin','Owner']

    form_class = DiscountForm
    initial = {"key": "value"}
    template_name = 'discounts/edit.html'

    def get(self, request, pk):
        discount = Discount.objects.get(pk=pk)
        # print(discount.__dict__)
        try:
            discount_items = discount.discounts.values_list('item_id', flat=True)
            order_type = discount.order_type.split(',') if discount.order_type else None
            store_id = request.user.storeowner.store.id
            store = Store.objects.filter(id=store_id)
            store_serializer = StoreSerializer(store, many=True, )
            data = store_serializer.data
            form = self.form_class(initial=model_to_dict(discount))
            return render(request, self.template_name, {'form': form,
                                                        'data': data,
                                                        'order_type': order_type,
                                                        'discount_items': discount_items,
                                                        'form_errors': form.errors})
        except:
            store = Store.objects.all()
            store_serializer = StoreSerializer(store, many=True, )
            order_type = discount.order_type.split(',') if discount.order_type else None
            data = store_serializer.data
            form = self.form_class(initial=model_to_dict(discount))

            return render(request, self.template_name, {'form': form,
                                                        'data': data,
                                                        'order_type': order_type,
                                                        'form_errors': form.errors})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        order_type = request.POST.getlist('order_type')
        item_list = request.POST.getlist('item_id')
        if form.is_valid():
            Discount.objects.filter(pk=pk).update(title=form.cleaned_data['title'],
                                                  type=form.cleaned_data['type'],
                                                  description=form.cleaned_data['description'],
                                                  terms_and_conditions=form.cleaned_data[
                                                      'terms_and_conditions'],
                                                  order_type=",".join(i for i in order_type),
                                                  validate_on_code=form.cleaned_data[
                                                      'validate_on_code'],
                                                  status=form.cleaned_data['status'],
                                                  from_date=form.cleaned_data['from_date'],
                                                  to_date=form.cleaned_data['to_date'],
                                                  # amount=form.cleaned_data['amount'],
                                                  from_time=form.cleaned_data['from_time'],
                                                  to_time=form.cleaned_data['to_time'],
                                                  code=form.cleaned_data['code'],
                                                  percentage=form.cleaned_data['percentage'],
                                                  add_on=form.cleaned_data['add_on'],
                                                  updated_on=timezone.now(),
                                                  created_by=request.user
                                                  )

            discount_config = Discount.objects.get(pk=pk)
            discount_items = list(discount_config.discounts.values_list('item_id', flat=True))
            discount_items = [str(i) for i in discount_items]

            if item_list:
                for i in item_list:
                    if i not in discount_items:
                        DiscountOnItem.objects.create(
                            discount_id=discount_config.id,
                            item_id=i
                        )

            return HttpResponseRedirect(reverse('custom-admin:discount_index'))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class DeleteDiscount(GroupRequiredMixin, APIView):
    group_required = ['Super admin','Owner']

    def get(self, request, pk):
        Discount.objects.filter(pk=pk).update(is_deleted=True)
        return JsonResponse({"status": True, 'message': "Discount Successfully Deleted!"})
