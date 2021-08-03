from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from pkbadmin.serializers.store_serializer import StoreSerializer
from pkbadmin.forms.taxes_forms import TaxesForm
from apps.stores.models import Store
from django.views import View
from pkbadmin.views.decorators import GroupRequiredMixin
from apps.taxconfig.models import Taxconfig, TaxOnItem
from libraries.DataTables import DataTables


class TaxIndex(GroupRequiredMixin, View):
    group_required = ['Super admin','Owner']
    template_name = 'taxes/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetTax(GroupRequiredMixin, View):
    group_required = ['Super admin','Owner']

    def post(self, request):
        user=request.user
        qs = Taxconfig.objects.filter(is_deleted=False,created_by=user)

        datatable = DataTables(request, Taxconfig)
        datatable.COLUMN_SEARCH = ['title', 'tax_type', 'order_type', 'amount']
        datatable.select('id', 'title', 'tax_type', 'order_type', 'value_type', 'amount', 'description')
        datatable.set_queryset(qs)

        return datatable.response()


class AddTax(GroupRequiredMixin, View):
    group_required = ['Owner']

    form_class = TaxesForm
    initial = {"key": "value"}
    template_name = 'taxes/create.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        store_id = request.user.storeowner.store.id
        store = Store.objects.filter(id=store_id)
        try:
            store_serializer = StoreSerializer(store,many=True)
            data = store_serializer.data
            if data is not None:
                return render(request, self.template_name, {'form': form, 'form_errors': form.errors,
                    'data': data})
        except Exception as e:
            # messages.success(request, "Please add items to apply tax!", extra_tags="")
            return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    def post(self, request):
        form = self.form_class(request.POST)
        order_type = request.POST.getlist('order_type')
        item_list = request.POST.getlist('item_id')
        if form.is_valid():
            taxconfig = Taxconfig.objects.create(
                title=form.cleaned_data['title'],
                tax_type=form.cleaned_data['tax_type'],
                order_type=",".join(i for i in order_type),
                amount=form.cleaned_data['amount'],
                value_type=form.cleaned_data['value_type'],
                description=form.cleaned_data['description'],
                created_on=timezone.now(),
                created_by=request.user,

            )
            if item_list:
                for i in item_list:
                    TaxOnItem.objects.create(
                        tax_id=taxconfig.id,
                        item_id=i
                    )

            return HttpResponseRedirect(reverse("custom-admin:taxes_index"))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class UpdateTax(GroupRequiredMixin, View):
    group_required = ['Owner']

    form_class = TaxesForm
    initial = {"key": "value"}
    template_name = 'taxes/edit.html'

    def get(self, request, pk):
        tax = Taxconfig.objects.get(pk=pk)
        try:
            tax_items = tax.taxes.values_list('item_id', flat=True)
            order_type = tax.order_type.split(',') if tax.order_type else None
            store_id = request.user.storeowner.store.id
            store = Store.objects.filter(id=store_id)
            store_serializer = StoreSerializer(store, many=True, )
            data = store_serializer.data
            form = self.form_class(initial=model_to_dict(tax))
            return render(request, self.template_name, {'form': form,
                                                        'form_errors': form.errors,
                                                        'data': data,
                                                        'order_type': order_type,
                                                        'tax_items': tax_items
                                                        })
        except:
            store_id = request.user.storeowner.store.id
            store = Store.objects.filter(id=store_id)
            store_serializer = StoreSerializer(store, many=True, )
            data = store_serializer.data
            form = self.form_class(initial=model_to_dict(tax))
            return render(request, self.template_name, {'form': form,
                                                        'form_errors': form.errors,
                                                        'data': data,
                                                        })

    def post(self, request, pk):
        form = self.form_class(request.POST)
        order_type = request.POST.getlist('order_type')
        item_list = request.POST.getlist('item_id')
        if form.is_valid():
            Taxconfig.objects.filter(pk=pk).update(
                title=form.cleaned_data['title'],
                tax_type=form.cleaned_data['tax_type'],
                order_type=",".join(i for i in order_type) if order_type else None,
                amount=form.cleaned_data['amount'],
                value_type=form.cleaned_data['value_type'],
                description=form.cleaned_data['description'],
                updated_on=timezone.now(),

            )

            taxconfig = Taxconfig.objects.get(pk=pk)
            tax_items = list(taxconfig.taxes.values_list('item_id', flat=True))
            tax_items = [str(i) for i in tax_items]
            if item_list:
                for i in item_list:
                    if i not in tax_items:
                        TaxOnItem.objects.create(
                            tax_id=taxconfig.id,
                            item_id=i
                        )

            return HttpResponseRedirect(reverse("custom-admin:taxes_index"))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class DeleteTax(GroupRequiredMixin, View):
    group_required = ['Owner']

    def get(self, request, pk):
        Taxconfig.objects.filter(pk=pk).update(is_deleted=True)
        return JsonResponse({"status": True, "message": "Tax Successfully Deleted!"})
