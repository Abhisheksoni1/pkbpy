from django.contrib.auth.decorators import login_required
from config import settings
from django.shortcuts import render
from apps.common.models import PushNotifications
from libraries.DataTables import DataTables
from django.views import View
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from pkbadmin.views.decorators import GroupRequiredMixin
from apps.users.models import LoginLog
from libraries.Push_notifications import notifications


class NotificationIndex(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'notifications/index.html'

    def get(self, request):
        return render(request, self.template_name)


class GetNotification(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        notification_data = PushNotifications.objects.filter(status=True)
        datatable = DataTables(request, PushNotifications)
        datatable.COLUMN_SEARCH = ['title']
        datatable.select('id', 'title', 'message', 'status', 'created_on', 'user__mobile')
        datatable.set_queryset(notification_data)

        return datatable.response()


class CreateNotification(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'notifications/create.html'
    initial = {"key": "value"}

    def get(self, request):
        return render(request, self.template_name)


class SendNotification(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        user_ids = request.POST.getlist('user_ids[]')
        message = request.POST.get('message')

        for user_id in user_ids:
            try:
                PushNotifications.objects.create(
                    title='notification',
                    message=message,
                    user_id=user_id,
                    created_on=timezone.now(),
                    updated_on=timezone.now()
                )
                login_log = LoginLog.objects.filter(user_id=user_id, status=True)

                for log in login_log:
                    notifications(log.device_token, message)

            except Exception as e:
                print(e)

        return JsonResponse({"status": True, 'message': "Notification has been successfully sent"})
