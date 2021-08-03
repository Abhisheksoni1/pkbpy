from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, logout, login, hashers
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render
from django.core import signing
from django.views import View

from apps.stores.models import StoreManager,KitchenManager
from pkbadmin.views.decorators import GroupRequiredMixin

from apps.orders.models import Order
from apps.users.models import User, Address, UserWalletLog
from django.http import HttpResponseServerError
import re
from config import settings
from libraries.DataTables import DataTables
from libraries.Email_model import send_auth_email
from libraries.Email_templates import get_user_registeration_verify_content, get_user_password_confirmation
from libraries.Functions import generate_password
from pkbadmin.forms.auth_forms import UserForgotPasswordForm, UserResetPasswordForm, ChangePasswordForm


# Create your views here.
def auth_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("custom-admin:index"))
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None and "Manager" in user.group_name:
            if user.is_active is True:
                if user.kitchenmanager.kitchen.is_deleted is True:
                    messages.error(request, 'Your kitchen no longer exists please contact store owner')
                    return HttpResponseRedirect(reverse("custom-admin:auth_login"))
            else:
                messages.error(request, 'You are no active manager please contact to store owner')
                return HttpResponseRedirect(reverse("custom-admin:auth_login"))
        # if user is not None and  "Owner" in user.group_name:
        #     if user.is_active is True :
        #         if user.storeowner.store.is_deleted is True:
        #             messages.error(request, 'Your store no longer exists please contact super admin')
        #             return HttpResponseRedirect(reverse("custom-admin:auth_login"))
        #     else:
        #         messages.error(request, 'You are no longer active owner please contact to admin')
        #         return HttpResponseRedirect(reverse("custom-admin:auth_login"))

        # if user is super admin
        if user is not None and user.is_staff != 0 and user.is_active == 1:
            login(request, user)

            messages.success(request, 'Successfully Logged-In', extra_tags="")
            return HttpResponseRedirect(reverse("custom-admin:index"))

        # if user is normal user for backend either Owner or Manager
        if user is not None and user.is_superuser == 0 and user.is_email_verified == 1 and user.is_active == 1:
            login(request, user)
            messages.success(request, 'Successfully Logged-In', extra_tags="")
            return HttpResponseRedirect(reverse("custom-admin:index"))

        elif user is not None and user.is_email_verified != 1:
            messages.error(request, 'Please verify your email id.', extra_tags="")
            return render(request, 'users/login.html')

        elif user is not None and user.is_active == 0:
            messages.error(request, 'You are not authorized to login.', extra_tags="")
            return render(request, 'users/login.html')

        else:
            messages.error(request, 'Email-Id / Password does not match.', extra_tags="")
            return render(request, 'users/login.html')

    else:
        return render(request, 'users/login.html')


def auth_logout(request):
    logout(request)
    messages.success(request, 'Successfully Logged-Out', extra_tags="")

    return HttpResponseRedirect(reverse("custom-admin:auth_login"))


def UserRegisterVerify(request):
    token = request.GET.get('token')
    data = signing.loads(token)

    try:
        user_data = User.objects.get(id=data['id'], email=data['email'], is_active=1)

        user = User.objects.filter(id=data['id'], email=data['email'], is_active=1).update(is_email_verified=1)

        if user:
            messages.success(request, "User email id successfully verified.", extra_tags="")
            return HttpResponseRedirect(reverse('custom-admin:auth_login'))
        else:
            raise HttpResponseServerError()

    except Exception as e:
        print("Error in Mail???", str(e))
        status = False

    return status


class UserPasswordForgot(View):
    form_class = UserForgotPasswordForm
    initial = {"key": "value"}
    template_name = 'users/forget_password.html'
    response = ""

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                email = form.cleaned_data['email']
                user = User.objects.get(email=email)
                if user:
                    token_data = {
                        'id': user.id,
                        'email': user.email
                    }
                    token = signing.dumps(token_data)
                    link = (settings.BASE_URL, 'admin/reset-password/?token=', token)
                    link = ''.join(link)
                    data = {
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'user_name': user.email,
                        'link': link
                    }
                    body = get_user_registeration_verify_content(request, data)
                    receiver = user.email
                    subject = "Password Reset Link"
                    User.objects.filter(id=user.id).update(password_reset_token=token)
                    send_auth_email.delay(subject, body, receiver)
                    messages.success(request, 'We have sent password reset link to your email', extra_tags="")

                    self.response = HttpResponseRedirect(reverse("custom-admin:auth_login"))
            else:
                self.response = render(request, self.template_name, {'form': form, 'form_errors': form.errors})

        except Exception as e:
            print(e)
            self.response = render(request, self.template_name,
                                   {'form': form, 'errors': "User email has not been registered."})

        return self.response


class UserPasswordConfirm(View):
    form_class = UserResetPasswordForm
    template_name = 'users/password_reset.html'
    initial = {"key": "value"}

    def get(self, request):
        form = self.form_class(initial=self.initial)
        token = request.GET.get('token')
        data = signing.loads(token)
        if token == User.objects.get(id=data['id']).password_reset_token:
            return render(request, self.template_name, {'form': form, 'data': data})
        return HttpResponseRedirect(reverse("custom-admin:auth_login"))

    def post(self, request):
        form = self.form_class(request.POST)
        email = request.POST.get('email')

        if form.is_valid():
            password = form.cleaned_data['password']
            User.objects.filter(email=email).update(password=hashers.make_password(password), password_reset_token='')

            data = User.objects.get(email=email)
            if "Manager" in data.group_name:
                KitchenManager.objects.filter(manager=data).update(manager_p=form.cleaned_data['password'])

            body = get_user_password_confirmation(request, data)
            receiver = email
            subject = "Password Reset Successfully."

            send_auth_email.delay(subject, body, receiver)
            messages.success(request, 'Password has been reset successfully', extra_tags="")
            return HttpResponseRedirect(reverse("custom-admin:auth_login"))
        return HttpResponseRedirect(reverse("custom-admin:auth_confirm"))


class ChangePassword(View):
    form_class = ChangePasswordForm
    initial = {"key": "value"}
    template_name = 'users/change_password.html'

    def get(self, request):
        form = self.form_class(initial=self.initial, user=request.user)
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})

    def post(self, request):
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            user_password = User.objects.get(id=request.user.id).password
            if hashers.check_password(current_password, user_password):
                User.objects.filter(id=request.user.id).update(
                    password=hashers.make_password(form.cleaned_data['password']))
                data = User.objects.get(id=request.user.id)
                if "Manager" in data.group_name:
                    StoreManager.objects.filter(manager=data).update(manager_p=form.cleaned_data['password'])
                body = get_user_password_confirmation(request, data)
                receiver = data.email
                subject = "Password Reset Successfully."
                send_auth_email.delay(subject, body, receiver)
                messages.success(request, 'Password has been reset successfully', extra_tags="")

                return HttpResponseRedirect(reverse("custom-admin:auth_login"))

            return HttpResponseRedirect(reverse("custom-admin:auth_change_password"))
        return render(request, self.template_name, {'form': form, 'form_errors': form.errors})


class UserProfile(GroupRequiredMixin, View):
    group_required = ['Super admin']
    template_name = 'users/user_profile.html'

    def get(self, request, pk):
        users = User.objects.get(pk=pk)
        try:
            addresses = Address.objects.filter(user_id=pk)
            user_wallet_log = UserWalletLog.objects.filter(user_id=pk)
            return render(request, self.template_name, {"users": users,
                                                        "addresses": addresses,
                                                        "user_wallet_log": user_wallet_log
                                                        })
        except:
            return render(request, self.template_name, {"users": users
                                                        })


class GetOrders(GroupRequiredMixin, View):
    group_required = ['Super admin']

    def post(self, request):
        user_id = request.POST.get('user_id')
        qs = Order.objects.filter(user_id=user_id)

        datatable = DataTables(request, Order)
        datatable.COLUMN_SEARCH = ['order_no', 'user__name', 'user__mobile', 'delivery_address']
        datatable.select('id', 'order_no', 'user__name', 'user__mobile', 'grand_total', 'delivery_address',
                         'created_on', 'order_status', 'status')
        datatable.set_queryset(qs)
        # print(datatable.set_queryset(qs))
        return datatable.response()


def erro_404(request):
    return render(request, '404.html')
