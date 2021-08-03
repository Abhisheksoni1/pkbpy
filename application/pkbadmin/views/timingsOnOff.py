from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.stores.models import Kitchen, Store
from pkbadmin.views.decorators import GroupRequiredMixin


class TimingKitchen(GroupRequiredMixin, View):
    group_required = ['Manager','Owner']
    template_name = 'timings/kitchen_timings.html'

    def get(self, request):
        if "Manager" in request.user.group_name:
            kitchens = Kitchen.objects.filter(manager__manager=request.user,is_deleted=False)
        else:
            kitchens = Kitchen.objects.filter(created_by=request.user,is_deleted=False)

        return render(request, self.template_name, {'kitchens': kitchens})


class UpdateKitchenStatus(GroupRequiredMixin, View):
    group_required = ['Manager','Owner']

    def post(self, request):
        kitchen_id = request.POST.get('kitchen_id')
        status = Kitchen.objects.get(id=kitchen_id).status
        if status:
            Kitchen.objects.filter(id=kitchen_id).update(status=False)
        else:
            Kitchen.objects.filter(id=kitchen_id).update(status=True)
        return JsonResponse({'status': True, 'message': 'Kitchen status changed successfully.'})


class TimingStore(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'timings/store_timings.html'

    def get(self, request):
        stores = Store.objects.all()
        return render(request, self.template_name, {'stores': stores})


class UpdateStoreStatus(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        store_id = request.POST.get('store_id')
        status = Store.objects.get(id=store_id).status
        if status:
            Store.objects.filter(id=store_id).update(status=False)
            kitchen = Kitchen.objects.filter(store_id=store_id)
            for kitchen in kitchen:
                kitchen.status = False
                kitchen.save()
        else:
            Store.objects.filter(id=store_id).update(status=True)
            kitchen = Kitchen.objects.filter(store_id=store_id)
            for kitchen in kitchen:
                kitchen.status = True
                kitchen.save()

        return JsonResponse({'status': True, 'message': 'Store status changed successfully.'})
