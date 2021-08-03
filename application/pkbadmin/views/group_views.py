from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from pkbadmin.views.decorators import GroupRequiredMixin
from config import settings
from libraries.DataTables import DataTables
from pkbadmin.forms.group_forms import GroupForm
from rest_framework.views import APIView


class GroupsIndex(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'groups/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetGroups(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        qs = Group.objects.all()
        datatable = DataTables(request, Group)
        datatable.COLUMN_SEARCH = ['name']
        datatable.select('id', 'name', )
        datatable.set_queryset(qs)

        return datatable.response()


class AddGroup(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = GroupForm
    template_name = 'groups/create.html'
    initial = {"key": "value"}
    permissions = Permission.objects.all()

    def get(self, request):
        form = self.form_class(initial=self.initial)
        permissions = self.permissions
        return render(request, self.template_name,
                      {'form': form, 'form_errors': form.errors, 'permissions': permissions})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            permissions = request.POST.getlist('perms_select_box_ids')
            if permissions:
                try:
                    group = Group.objects.create(name=form.cleaned_data['name'])
                    group.permissions.add(*permissions)
                except Exception as e:
                    permissions = self.permissions
                    return render(request, self.template_name,
                                  {'form': form, 'form_errors': form.errors,
                                   'errors': 'This name has already been taken.',
                                   'permissions': permissions})

            else:
                try:
                    Group.objects.create(name=form.cleaned_data['name'])
                    return HttpResponseRedirect(reverse("custom-admin:group_index"))
                except Exception as e:
                    permissions = Permission.objects.all()
                    return render(request, self.template_name,
                                  {'form': form, 'form_errors': form.errors,
                                   'errors': 'This name has already been taken.',
                                   'permissions': permissions
                                   })
            return HttpResponseRedirect(reverse("custom-admin:group_index"))

        return HttpResponseRedirect(reverse("custom-admin:add_group"))


class UpdateGroup(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = GroupForm
    initial = {"key": "value"}
    template_name = 'groups/edit.html'
    permissions = Permission.objects.all()

    def get(self, request, pk):
        group = Group.objects.get(pk=pk)
        permissions = self.permissions
        assigned_permission = group.permissions.all()
        assigned_permissions = list(assigned_permission.values('id', 'name'))
        form = self.form_class(initial=model_to_dict(group))
        return render(request, self.template_name,
                      {'form': form, 'form_errors': form.errors, 'permissions': permissions,
                       'assigned_permissions': assigned_permissions})

    def post(self, request, pk):
        group = Group.objects.get(pk=pk)
        group.permissions.clear()
        form = self.form_class(request.POST)
        if form.is_valid():
            permissions = request.POST.getlist('perms_select_box_ids')
            if permissions:
                try:
                    Group.objects.filter(pk=pk).update(name=form.cleaned_data['name'])
                    group = Group.objects.get(pk=pk)
                    group.permissions.add(*permissions)
                except Exception as e:
                    permissions = self.permissions
                    return render(request, self.template_name,
                                  {'form': form, 'form_errors': form.errors,
                                   'errors': 'This name has already been taken.',
                                   'permissions': permissions})

            else:
                try:
                    Group.objects.filter(pk=pk).update(name=form.cleaned_data['name'])
                    return HttpResponseRedirect(reverse("custom-admin:group_index"))
                except Exception as e:
                    permissions = Permission.objects.all()
                    return render(request, self.template_name,
                                  {'form': form, 'form_errors': form.errors,
                                   'errors': 'This name has already been taken.',
                                   'permissions': permissions
                                   })
            return HttpResponseRedirect(reverse("custom-admin:group_index"))
        return HttpResponseRedirect(reverse("custom-admin:group_index"))


class DeleteGroup(GroupRequiredMixin, APIView):
    group_required = ['Super admin']

    def get(self, request, pk):
        Group.objects.filter(pk=pk).delete()
        return Response({"status": True, 'message': "Group Successfully Deleted!"})
