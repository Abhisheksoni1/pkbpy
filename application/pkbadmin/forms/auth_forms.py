from datetime import time
from django.template.loader import render_to_string
from config import settings
from django import forms
from django.core import signing
from django.contrib.auth.backends import UserModel
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from libraries.Functions import base_token_factory
import re
from apps.users.models import User
from django.contrib.auth import authenticate, logout, login, hashers


class UserForgotPasswordForm(forms.Form):
    email = forms.CharField(
        required=False,
        max_length=100,
        error_messages={'required': 'Please enter your email.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required email',
            'data-validation-error-msg-required': "Please enter your registered mail id.",
            'data-validation-error-msg-email': "Please enter valid mail id.",
            'placeholder': 'Email Id',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if EmailValidator(message='Invalid email id.')(email):
            raise ValidationError('Invalid email id.')
        else:
            return email


class UserResetPasswordForm(forms.Form):
    password = forms.CharField(
        required=False,
        max_length=15,
        error_messages={'required': 'Please enter new password.'},
        widget=forms.PasswordInput(attrs={'data-validation': 'required', 'placeholder': 'New Password'})
    )

    repeat_password = forms.CharField(
        required=False,
        max_length=15,
        error_messages={'required': 'Please enter confirm password.'},
        widget=forms.PasswordInput(
            attrs={'data-validation': 'required confirmation', 'data-validation-confirm': 'password',
                   'placeholder': 'Retype Password'})
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password is None:
            raise ValidationError('Invalid password.')
        elif not re.match("^[a-zA-Z0-9!@#$&()\\-`.+,/\"]*$", password):
            raise ValidationError('Password is too weak. Ex : A@1art')
        else:
            return password

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise ValidationError('Password does not match.')
        else:
            return repeat_password


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        max_length=15,
        required=False,
        error_messages={'required': 'Please enter the current password.'},
        widget=forms.PasswordInput(attrs={
            'data-validation': 'required',
            'data-validation-error-msg': "Please enter your current password.",
            'placeholder': 'Current Password'})
    )

    password = forms.CharField(
        required=False,
        max_length=15,
        error_messages={'required': 'Please enter new password.'},
        widget=forms.PasswordInput(attrs={
            'data-validation': 'required',
            'data-validation-error-msg': "Please enter your new password.",
            'placeholder': 'New Password'})
    )

    repeat_password = forms.CharField(
        required=False,
        max_length=15,
        error_messages={'required': 'Please enter confirm password.'},
        widget=forms.PasswordInput(
            attrs={
                'data-validation': 'required confirmation',
                'data-validation-confirm': 'password',
                'data-validation-error-msg': "New password and repeat password does not match",
                'placeholder': 'Retype Password'
            })
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password is None:
            raise ValidationError('Invalid password.')
        elif not re.match("^[a-zA-Z0-9!@#$&()\\-`.+,/\"]*$", password):

            raise ValidationError('Password is too weak. you can choose alphanumeric and special among[!@#$&()]')
        else:
            return password

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise ValidationError('Password does not match.')
        else:
            return repeat_password

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user_password = User.objects.get(id=user.id).password

    def clean_current_password(self):
        user_password = self.user_password
        password = self.cleaned_data['current_password']
        if not hashers.check_password(password, user_password):
            raise ValidationError('Current password does not match with existing password')
        return password

