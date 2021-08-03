from django.shortcuts import render
from libraries.DataTables import DataTables
from apps.feedback.models import OrderFeedback, KitchenFeedback
from pkbadmin.views.decorators import GroupRequiredMixin
from django.views import View


class OrderFeedbackIndex(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']
    template_name = 'feedback/order_index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetOrderFeedback(GroupRequiredMixin, View):
    group_required = [ 'Manager']

    def post(self, request):
        kitchen = request.user.kitchenmanager.kitchen

        qs = OrderFeedback.objects.filter(order__kitchen=kitchen)
        datatable = DataTables(request, OrderFeedback)
        datatable.COLUMN_SEARCH = ['order__order_no', 'message', 'order__user__mobile']
        datatable.select('id', 'order__order_no', 'message', 'rating', 'order__user__mobile', 'status')
        datatable.set_queryset(qs)
        return datatable.response()


class KitchenFeedbackIndex(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']
    template_name = 'feedback/kitchen_index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetKitchenFeedback(GroupRequiredMixin, View):
    group_required = ['Manager']

    def post(self, request):
        kitchen = request.user.kitchenmanager.kitchen
        qs = KitchenFeedback.objects.filter(kitchen_id=kitchen.id)

        datatable = DataTables(request, OrderFeedback)
        datatable.COLUMN_SEARCH = ['kitchen_id__name', 'message']
        datatable.select('id', 'kitchen_id__name', 'message', 'status')
        datatable.set_queryset(qs)
        return datatable.response()
