from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from apps.common.models import FinancialYear
from pkbadmin.views.decorators import GroupRequiredMixin


class FinancialYearAdd(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'settings/financial_year.html'

    def get(self, request):
        try:
            financial_year = FinancialYear.objects.latest('id')
            fyear = financial_year.financial_year
            return render(request, self.template_name, {'fyear': fyear})
        except:
            return render(request, self.template_name)

    def post(self, request):
        year = request.POST.get('financial_year')
        try:
            fyear = FinancialYear.objects.latest('id')
            if fyear:
                FinancialYear.objects.filter(id=fyear.id).update(
                    financial_year=year,
                    updated_on=timezone.now(),
                )
                return HttpResponseRedirect(reverse("custom-admin:index"))

        except:
            FinancialYear.objects.create(

                financial_year=year,
                created_on=timezone.now(),
                created_by=request.user

            )
            return HttpResponseRedirect(reverse("custom-admin:index"))
