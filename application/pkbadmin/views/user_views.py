from rest_framework.response import Response
from libraries.DataTables import DataTables
from django.shortcuts import render
from apps.users.models import User
from rest_framework.views import APIView
from pkbadmin.views.decorators import GroupRequiredMixin
from django.views import View


class UsersIndex(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'users/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetUsers(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        data = User.objects.filter(is_active=True, groups__name='User')
        # data = User.objects.filter(is_active=True)
        datatable = DataTables(request, User)
        datatable.COLUMN_SEARCH = ['name', 'mobile']
        datatable.select('id', 'name', 'mobile', 'last_login', 'is_active', 'userwallet__amount')
        datatable.set_queryset(data)

        return datatable.response()


class DeactivateUser(GroupRequiredMixin, APIView):
    group_required = ['Super admin']

    def get(self, request, pk):
        User.objects.filter(pk=pk).update(is_active=False)
        return Response({"status": True, 'message': "User Successfully Deactivated!"})
