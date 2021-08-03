from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from pkbadmin.views.decorators import GroupRequiredMixin
from datetime import timedelta
from apps.orders.models import Order
from django.views import View
from apps.stores.models import Kitchen, StoreManager, StoreOwner, Store
from datetime import date
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse


class DashboardIndex(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager', 'Owner']

    def get(self, request):
        qs = get_user_model().objects.filter(is_staff=0, groups__name='User', is_active=1)
        if request.user.is_superuser:
            store = Store.objects.all()
            today_date = date.today()
            store_kitchen = [store for store in store if store.kitchens.all().count() != 0]
            kitchen = Kitchen.objects.all()
            order = Order.objects.all()
            month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            pending_order_monthly = []
            confirmed_order_monthly = []
            delivered_order_monthly = []
            declined_order_monthly = []
            for i in month_list:
                pending_order_monthly.append(
                    len(Order.objects.filter(order_status=Order.ORDER_STATUS_PENDING, created_on__year=today_date.year,
                                             created_on__month=i,
                                             )))
                confirmed_order_monthly.append(
                    len(Order.objects.filter(order_status=Order.ORDER_STATUS_CONFIRMED,
                                             created_on__year=today_date.year, created_on__month=i,
                                             )))
                delivered_order_monthly.append(
                    len(Order.objects.filter(order_status=Order.ORDER_STATUS_DELIVERED,
                                             created_on__year=today_date.year, created_on__month=i,
                                             )))
                declined_order_monthly.append(
                    len(Order.objects.filter(order_status=Order.ORDER_STATUS_DECLINED, created_on__year=today_date.year,
                                             created_on__month=i,
                                             )))

            context = {
                'total_users': len(qs),
                'total_orders': len(order),
                'store': store_kitchen,
                'kitchen': kitchen,
                'pending_order_month': pending_order_monthly,
                'confirmed_order_month': confirmed_order_monthly,
                'delivered_order_month': delivered_order_monthly,
                'declined_order_month': declined_order_monthly,

            }

            return render(request, "dashboard/index.html", context)


        elif "Manager" in request.user.group_name:
            id = request.user.kitchenmanager.kitchen.id
            kitchen = Kitchen.objects.filter(id=id)
            today_date = date.today()
            kitchen_id = [k.id for k in kitchen]
            order = Order.objects.filter(kitchen_id__in=kitchen_id)
            day_order = Order.objects.filter(created_on__date=today_date, kitchen_id__in=kitchen_id)
            week_order = Order.objects.filter(created_on__gte=(timezone.now().date() - timedelta(days=7)),
                                              kitchen_id__in=kitchen_id)
            month_order = Order.objects.filter(created_on__gte=(timezone.now().date() - timedelta(days=30)),
                                               kitchen_id__in=kitchen_id)

            pending_order_week = Order.objects.filter(order_status=Order.ORDER_STATUS_PENDING,
                                                      created_on__gte=(timezone.now().date() - timedelta(days=7)),
                                                      kitchen_id__in=kitchen_id)

            confirmed_order_week = Order.objects.filter(order_status=Order.ORDER_STATUS_CONFIRMED,
                                                        created_on__gte=(timezone.now().date() - timedelta(days=7)),
                                                        kitchen_id__in=kitchen_id
                                                        )
            delivered_order_week = Order.objects.filter(order_status=Order.ORDER_STATUS_DELIVERED,
                                                        created_on__gte=(timezone.now().date() - timedelta(days=7)),
                                                        kitchen_id__in=kitchen_id
                                                        )
            declined_order_week = Order.objects.filter(order_status=Order.ORDER_STATUS_DECLINED,
                                                       created_on__gte=(timezone.now().date() - timedelta(days=7)),
                                                       kitchen_id__in=kitchen_id
                                                       )

            pending_order_daily = Order.objects.filter(order_status=Order.ORDER_STATUS_PENDING,
                                                       created_on__date=today_date, kitchen_id__in=kitchen_id
                                                       )
            confirmed_order_daily = Order.objects.filter(order_status=Order.ORDER_STATUS_CONFIRMED,
                                                         created_on__date=today_date, kitchen_id__in=kitchen_id
                                                         )
            delivered_order_daily = Order.objects.filter(order_status=Order.ORDER_STATUS_DELIVERED,
                                                         created_on__date=today_date, kitchen_id__in=kitchen_id
                                                         )
            declined_order_daily = Order.objects.filter(order_status=Order.ORDER_STATUS_DECLINED,
                                                        created_on__date=today_date, kitchen_id__in=kitchen_id)

            month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

            pending_order_monthly = []
            confirmed_order_monthly = []
            delivered_order_monthly = []
            declined_order_monthly = []
            for i in month_list:
                pending_order_monthly.append(
                    len(Order.objects.filter(order_status=Order.ORDER_STATUS_PENDING, kitchen_id__in=kitchen_id,
                                             created_on__year=today_date.year, created_on__month=i,
                                             )))
                confirmed_order_monthly.append(
                    len(Order.objects.filter(order_status=Order.ORDER_STATUS_CONFIRMED, kitchen_id__in=kitchen_id,
                                             created_on__year=today_date.year, created_on__month=i,
                                             )))
                delivered_order_monthly.append(
                    len(Order.objects.filter(order_status=Order.ORDER_STATUS_DELIVERED, kitchen_id__in=kitchen_id,
                                             created_on__year=today_date.year, created_on__month=i,
                                             )))
                declined_order_monthly.append(
                    len(Order.objects.filter(order_status=Order.ORDER_STATUS_DECLINED, kitchen_id__in=kitchen_id,
                                             created_on__year=today_date.year, created_on__month=i,
                                             )))

            context = {
                'kitchen': kitchen,
                'kitchen_list': [kitchen.id for kitchen in kitchen],
                'total_users': len(qs),
                'total_orders': len(order),
                'week_order': len(week_order),
                'month_order': len(month_order),
                'today_order': len(day_order),
                'pending_order_month': pending_order_monthly,
                'confirmed_order_month': confirmed_order_monthly,
                'delivered_order_month': delivered_order_monthly,
                'declined_order_month': declined_order_monthly,
                'pending_order_week': len(pending_order_week),
                'confirmed_order_week': len(confirmed_order_week),
                'delivered_order_week': len(delivered_order_week),
                'declined_order_week': len(declined_order_week),
                'pending_order_daily': len(pending_order_daily),
                'confirmed_order_daily': len(confirmed_order_daily),
                'delivered_order_daily': len(delivered_order_daily),
                'declined_order_daily': len(declined_order_daily),

            }

            return render(request, "dashboard/manager.html", context)

        elif "Owner" in request.user.group_name:
            try:

                store_owner = StoreOwner.objects.get(owner=request.user)
                store = store_owner.store
                today_date = date.today()
                kitchen = Kitchen.objects.filter(store_id=store.id)
                order = Order.objects.all()
                month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                pending_order_monthly = []
                confirmed_order_monthly = []
                delivered_order_monthly = []
                declined_order_monthly = []
                for i in month_list:
                    pending_order_monthly.append(
                        len(Order.objects.filter(order_status=Order.ORDER_STATUS_PENDING, created_on__year=today_date.year,
                                                 created_on__month=i, kitchen__store_id=store.id
                                                 )))
                    confirmed_order_monthly.append(
                        len(Order.objects.filter(order_status=Order.ORDER_STATUS_CONFIRMED,
                                                 created_on__year=today_date.year, created_on__month=i,
                                                 kitchen__store_id=store.id
                                                 )))
                    delivered_order_monthly.append(
                        len(Order.objects.filter(order_status=Order.ORDER_STATUS_DELIVERED,
                                                 created_on__year=today_date.year, created_on__month=i,
                                                 kitchen__store_id=store.id
                                                 )))
                    declined_order_monthly.append(
                        len(Order.objects.filter(order_status=Order.ORDER_STATUS_DECLINED, created_on__year=today_date.year,
                                                 created_on__month=i, kitchen__store_id=store.id
                                                 )))

                context = {
                    'total_users': len(qs),
                    'total_orders': len(order),
                    'store': store,
                    'kitchen': kitchen,
                    'pending_order_month': pending_order_monthly,
                    'confirmed_order_month': confirmed_order_monthly,
                    'delivered_order_month': delivered_order_monthly,
                    'declined_order_month': declined_order_monthly,
                    'user': request.user,
                    'bool':True

                }
                return render(request, "dashboard/owner.html", context)
            except Exception as e:
                """ bool to make sure we haven't addeded store yet"""
                context = {
                    'total_users': len(qs),
                    'total_orders': 0,
                    'store': [],
                    'kitchen': [],
                    'pending_order_month': 0,
                    'confirmed_order_month': 0,
                    'delivered_order_month': 0,
                    'declined_order_month': 0,
                    'user': request.user,
                    'bool':False


                }

                return render(request, "dashboard/owner.html", context)


class GetFilterOrder(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager', 'Owner']

    def post(self, request):
        order_type = request.POST.get('order_type')
        kitchen_id = request.POST.get('kitchen_id')
        response = {'status': False, 'msg': '', 'data': {}}
        today_date = date.today()
        # print(request.user)

        if order_type == "weekly":
            pending_order_week = Order.objects.filter(order_status=Order.ORDER_STATUS_PENDING,
                                                      created_on__gte=(timezone.now().date() - timedelta(days=7))
                                                      )
            if kitchen_id:
                pending_order_week = pending_order_week.filter(kitchen_id=kitchen_id)

            confirmed_order_week = Order.objects.filter(order_status=Order.ORDER_STATUS_CONFIRMED,
                                                        created_on__gte=(timezone.now().date() - timedelta(days=7)),
                                                        )
            if kitchen_id:
                confirmed_order_week = confirmed_order_week.filter(kitchen_id=kitchen_id)
            delivered_order_week = Order.objects.filter(order_status=Order.ORDER_STATUS_DELIVERED,
                                                        created_on__gte=(timezone.now().date() - timedelta(days=7)),
                                                        )
            if kitchen_id:
                delivered_order_week = delivered_order_week.filter(kitchen_id=kitchen_id)
            declined_order_week = Order.objects.filter(order_status=Order.ORDER_STATUS_DECLINED,
                                                       created_on__gte=(timezone.now().date() - timedelta(days=7)),
                                                       )
            if kitchen_id:
                declined_order_week = declined_order_week.filter(kitchen_id=kitchen_id)
            response['status'] = True
            response['data'] = {
                'pending_order': len(pending_order_week),
                'confirmed_order': len(confirmed_order_week),
                'delivered_order': len(delivered_order_week),
                'declined_order': len(declined_order_week),
            }

        elif order_type == "daily":
            pending_order_daily = Order.objects.filter(order_status=Order.ORDER_STATUS_PENDING,
                                                       created_on__date=today_date
                                                       )
            if kitchen_id:
                pending_order_daily = pending_order_daily.filter(kitchen_id=kitchen_id)

            confirmed_order_daily = Order.objects.filter(order_status=Order.ORDER_STATUS_CONFIRMED,
                                                         created_on__date=today_date
                                                         )
            if kitchen_id:
                confirmed_order_daily = confirmed_order_daily.filter(kitchen_id=kitchen_id)

            delivered_order_daily = Order.objects.filter(order_status=Order.ORDER_STATUS_DELIVERED,
                                                         created_on__date=today_date
                                                         )
            if kitchen_id:
                delivered_order_daily = delivered_order_daily.filter(kitchen_id=kitchen_id)
            declined_order_daily = Order.objects.filter(order_status=Order.ORDER_STATUS_DECLINED,
                                                        created_on__date=today_date,
                                                        )
            if kitchen_id:
                declined_order_daily = declined_order_daily.filter(kitchen_id=kitchen_id)
            response['status'] = True
            response['data'] = {
                'pending_order': len(pending_order_daily),
                'confirmed_order': len(confirmed_order_daily),
                'delivered_order': len(delivered_order_daily),
                'declined_order': len(declined_order_daily),

            }

        else:
            response['status'] = False
            response['msg'] = 'Some error occurred ! Please reload the page.'

        return JsonResponse(response)


class GetKitchenOrderFilter(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']

    def post(self, request):
        kitchen_id = request.POST.get('kitchen_id')

        response = {'status': False, 'msg': '', 'data': {}}
        today_date = date.today()

        month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        pending_order_monthly = []
        confirmed_order_monthly = []
        delivered_order_monthly = []
        declined_order_monthly = []
        for i in month_list:
            pending_order_monthly.append(
                len(Order.objects.filter(order_status=Order.ORDER_STATUS_PENDING, kitchen_id=kitchen_id,
                                         created_on__year=today_date.year, created_on__month=i,
                                         )))
            confirmed_order_monthly.append(
                len(Order.objects.filter(order_status=Order.ORDER_STATUS_CONFIRMED, kitchen_id=kitchen_id,
                                         created_on__year=today_date.year, created_on__month=i,
                                         )))
            delivered_order_monthly.append(
                len(Order.objects.filter(order_status=Order.ORDER_STATUS_DELIVERED, kitchen_id=kitchen_id,
                                         created_on__year=today_date.year, created_on__month=i,
                                         )))
            declined_order_monthly.append(
                len(Order.objects.filter(order_status=Order.ORDER_STATUS_DECLINED, kitchen_id=kitchen_id,
                                         created_on__year=today_date.year, created_on__month=i,
                                         )))

        response['status'] = True
        response['data'] = {
            'pending_order': pending_order_monthly,
            'confirmed_order': confirmed_order_monthly,
            'delivered_order': delivered_order_monthly,
            'declined_order': delivered_order_monthly,
        }

        return JsonResponse(response)
