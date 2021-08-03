from django.http import JsonResponse
from django.views import View
from pkbadmin.views.decorators import GroupRequiredMixin
from django.shortcuts import render
from apps.users.models import  User, UserWallet,UserWalletLog


class ManagePointIndex(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'managepoints/index.html'

    def get(self, request):
        return render(request, self.template_name)




class UpdateWallet(GroupRequiredMixin, View):
    group_required = ['Super admin']
    def post(self, request):

        response = {'status': False, 'msg': '', 'data': {}}

        user_ids = request.POST.getlist('user_ids[]')
        print(request.POST)
        points=request.POST.get('points')
        print(user_ids, points)

        for user_id in user_ids:
            uw= UserWallet.objects.get(user_id=user_id)
            uw.amount+=int(points)
            uw.save()
            UserWalletLog.objects.create(user_id=user_id,amount=+int(points))


        response['status'] = True
        response['msg'] = 'wallet update sussessfully'

        return JsonResponse(response)