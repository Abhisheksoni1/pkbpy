from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.utils import timezone
from apps.common.models import Faqs
from libraries.DataTables import DataTables
from pkbadmin.forms.faq_forms import FaqsForm
from pkbadmin.views.decorators import GroupRequiredMixin


class FaqsIndex(GroupRequiredMixin, View):
    template_name = 'faqs/index.html'
    group_required = ['Super admin']

    def get(self, request):
        return render(request, self.template_name)


class GetFaqs(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        qs = Faqs.objects.filter(is_deleted=False)

        datatable = DataTables(request, Faqs)
        datatable.COLUMN_SEARCH = ['question', 'short_answer', 'answer']
        datatable.select('id', 'question', 'short_answer', 'answer', 'status')
        datatable.set_queryset(qs)

        return datatable.response()


class AddFaqs(GroupRequiredMixin, View):
    group_required = ['Super admin']

    # permission_denied_message = "You don't have permission."

    form_class = FaqsForm
    initial = {"key": "value"}
    template_name = 'faqs/create.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            Faqs.objects.create(
                question=form.cleaned_data['question'],
                short_answer=form.cleaned_data['short_answer'],
                answer=form.cleaned_data['answer'],
                created_on=timezone.now(),
                created_by=request.user
            )
            return HttpResponseRedirect(reverse('custom-admin:faqs_index'))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class UpdateFaqs(GroupRequiredMixin, View):
    group_required = ['Super admin']

    form_class = FaqsForm
    initial = {"key": "value"}
    template_name = 'faqs/edit.html'

    def get(self, request, pk):
        obj = Faqs.objects.get(pk=pk)
        form = self.form_class(initial=model_to_dict(obj))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            Faqs.objects.filter(pk=pk).update(
                question=form.cleaned_data['question'],
                short_answer=form.cleaned_data['short_answer'],
                answer=form.cleaned_data['answer'],
                updated_on=timezone.now()
            )
            return HttpResponseRedirect(reverse('custom-admin:faqs_index'))

        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class DeleteFaqs(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def get(self, request, pk):
        Faqs.objects.filter(pk=pk).update(is_deleted=True)
        return JsonResponse({"status": True, "message": "Faqs Successfully Deleted!"})
