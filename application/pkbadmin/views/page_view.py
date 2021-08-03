from django.shortcuts import render
from django.urls import reverse

from config import settings
from django.views import View
# from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from pkbadmin.forms.page_forms import PageForm
from apps.common.models import Page
from django.contrib.auth.decorators import login_required
from libraries.DataTables import DataTables
from rest_framework.views import APIView
from rest_framework.response import Response
from libraries.Functions import image_upload_handler, make_dir, join_string
import os
from datetime import datetime
from django.utils import timezone
from pkbadmin.views.decorators import GroupRequiredMixin


class PageIndex(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'pages/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetPage(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        qs = Page.objects.filter(is_deleted=False, status=True)

        datatable = DataTables(request, Page)
        datatable.COLUMN_SEARCH = ['title']
        datatable.select('id', 'title', 'description', 'keywords', 'content')
        datatable.set_queryset(qs)

        return datatable.response()


class AddPage(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = PageForm
    initial = {"key": "value"}
    template_name = 'pages/create.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'errors': form.errors})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        current_user = request.user
        if form.is_valid():
            title = form.cleaned_data['title']
            page_title = join_string(title)
            image_path = make_dir(settings.MEDIA_ROOT + 'pages/' + page_title + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'])
            page = Page.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                content=form.cleaned_data['content'],
                keywords=form.cleaned_data['keywords'],
                status=form.cleaned_data['status'],
                created_on=timezone.now(), created_by=current_user
            )
            if request.FILES:
                img_path = image_upload_handler(request.FILES['image'], image_path)
                full_path = "{}".format(img_path)
                page.image = full_path
                page.save()
            return HttpResponseRedirect(reverse("custom-admin:page_main"))

        return render(request, self.template_name, {'form': form, 'errors': form.errors})


class UpdatePage(GroupRequiredMixin, View):
    group_required = ['Super admin']
    form_class = PageForm
    initial = {"key": "value"}
    template_name = 'pages/edit.html'

    def get(self, request, pk):

        obj = Page.objects.get(pk=pk)
        obj.status = '1' if obj.status else '0'
        form = self.form_class(initial=obj.__dict__)
        page_title, page_image = obj.title, obj.image
        page_title = join_string(page_title)
        if obj.image:
            image_path = os.path.join('pages', page_title, settings.CUSTOM_DIRS['IMAGE_DIR'], page_image)
        else:
            image_path=None
        # image_full_path = '{}{}'.format(image_path, page_image)
        return render(request, self.template_name, {'form': form, 'errors': form.errors, 'image_path': image_path})

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            page_title = Page.objects.get(pk=pk).title
            image_path = make_dir(settings.MEDIA_ROOT + 'pages/' + page_title + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'])
            if request.FILES.get('image'):
                img_path = image_upload_handler(request.FILES['image'], image_path)
                full_path = "{}".format(img_path)

                Page.objects.filter(pk=pk).update(title=form.cleaned_data['title'],
                                                  description=form.cleaned_data['description'],
                                                  content=form.cleaned_data['content'],
                                                  keywords=form.cleaned_data['keywords'],
                                                  status=form.cleaned_data['status'],
                                                  updated_on=timezone.now(),
                                                  image=full_path,
                                                  created_by=request.user)
            else:

                Page.objects.filter(pk=pk).update(title=form.cleaned_data['title'],
                                                  description=form.cleaned_data['description'],
                                                  content=form.cleaned_data['content'],
                                                  keywords=form.cleaned_data['keywords'],
                                                  status=form.cleaned_data['status'],
                                                  updated_on=timezone.now(),
                                                  created_by=request.user)

            return HttpResponseRedirect(reverse("custom-admin:page_main"))
        return render(request, self.template_name, {'form': form, 'errors': form.errors})


class DeletePage(GroupRequiredMixin, APIView):
    group_required = ['Super admin']

    def get(self, request, pk):
        Page.objects.filter(pk=pk).update(is_deleted=True)
        return Response({"status": True, 'message': "Page Successfully Deleted!"})

