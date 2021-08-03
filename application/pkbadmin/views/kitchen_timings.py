from django.http import JsonResponse
from django.shortcuts import render
from pkbadmin.views.decorators import SuperUserRequiredMixin
from django.views import View
from apps.stores.models import Kitchen


class TimingKitchen(SuperUserRequiredMixin, View):
    group_required = ['Manager']
    template_name = 'timings/kitchen_timings.html'

    def get(self, request):
        kitchens = Kitchen.objects.filter(store__manager__manager=request.user)

        return render(request, self.template_name, {'kitchens': kitchens})


class UpdateKitchenStatus(SuperUserRequiredMixin, View):
    group_required = ['Manager']

    def post(self, request):
        kitchen_id = request.POST.get('kitchen_id')
        status = Kitchen.objects.get(id=kitchen_id).status
        if status:

            Kitchen.objects.filter(id=kitchen_id).update(status=False)
        else:
            Kitchen.objects.filter(id=kitchen_id).update(status=True)
        return JsonResponse({'status': True, 'message': 'Kitchen status changed successfully.'})
