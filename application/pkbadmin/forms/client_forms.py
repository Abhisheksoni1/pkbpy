from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models import Q

from apps.users.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
class ClientForm(forms.Form):

    CHOICES = [
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other',  'Other')
            ]

    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength':"30",
            'class': "form-control",
            'data-validation':"custom",
            'data-validation-regexp' : "^([A-Za-z]+[,.]?[ ]?|[A-Za-z]+['-]?)+$",
            'data-validation-error-msg': "Last Name has to be an alphabet (max. 30 chars)."

        })
    )

    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': "30",
            'class': "form-control",
            'data-validation': "custom",
            'data-validation-regexp': "^([A-Za-z]+[,.]?[ ]?|[A-Za-z]+['-]?)+$",
            'data-validation-error-msg': "Last Name has to be an alphabet (max. 30 chars)."

        })
    )

    gender =forms.ChoiceField(choices=CHOICES,
                             widget=forms.RadioSelect(
                                 attrs={'data-validation':"required",
                                  'class':"custom-control-input radio",
                                 'data-validation-error-msg':"Gender is required field."
                                        }
                             )
                            )

    dob = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datepicker',
                # 'data-validation-error-msg-container': "#txtFromDate",
                'data-validation': "date",
                'data-validation-require-leading-zero': "false",
                'data-validation-error-msg': 'Date is required field and format should be yyyy-mm-dd.',
                'data-validation-format': "yyyy-mm-dd",

            }

            # years=range(1975, 2005)
        )
    )

    mobile = forms.CharField(
        max_length=2500,
        required=False,
        error_messages={'required': 'Please enter the answer.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'maxlength' :"10",
            'data-validation' : "number",
            'data-validation-allowing': "range[1000000000;9999999999]"
        }
        )
    )

    email = forms.CharField(
        required=False,
         max_length=100,
         widget=forms.TextInput(attrs={
             'class': "form-control",
             'data-validation' :"email"
         })
     )


    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if len(data)< 2:
            raise forms.ValidationError("Please Enter more than 2 characters")
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if len(data) < 4:
            raise forms.ValidationError("Please Enter more than 4 characters")
        return data

    def clean_mobile(self):
        value = self.cleaned_data['mobile']
        if not value:
            raise forms.ValidationError('mobile is required field.')
        else:
            try:

                if not User.objects.filter(mobile=value).exists():
                    if len(str(value)) != 10:
                        raise forms.ValidationError('mobile numer should be of 10 digits')
                    return value
                else:
                    raise forms.ValidationError('mobile number is already registered.')
            except Exception as error:
                raise error

    def clean_email(self):
        value = self.cleaned_data['email']

        if not value:
            raise forms.ValidationError('email is required field.')
        else:
            try:

                if not User.objects.filter(email=value).exists():
                    return value
                else:
                    raise forms.ValidationError('email id is already registered.')
            except Exception as error:
                raise error




class UpdateClientForm(forms.Form):

    CHOICES = [
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other',  'Other')
            ]

    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength':"30",
            'class': "form-control",
            'data-validation':"custom",
            'data-validation-regexp' : "^([A-Za-z]+[,.]?[ ]?|[A-Za-z]+['-]?)+$",
            'data-validation-error-msg': "Last Name has to be an alphabet (max. 30 chars)."

        })
    )

    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': "30",
            'class': "form-control",
            'data-validation': "custom",
            'data-validation-regexp': "^([A-Za-z]+[,.]?[ ]?|[A-Za-z]+['-]?)+$",
            'data-validation-error-msg': "Last Name has to be an alphabet (max. 30 chars)."

        })
    )

    gender =forms.ChoiceField(choices=CHOICES,
                             widget=forms.RadioSelect(
                                 attrs={'data-validation':"required",
                                  'class':"custom-control-input radio",
                                 'data-validation-error-msg':"Gender is required field."
                                        }
                             )
                            )

    dob = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datepicker',
                # 'data-validation-error-msg-container': "#txtFromDate",
                'data-validation': "date",
                'data-validation-require-leading-zero': "false",
                'data-validation-error-msg': 'Date is required field and format should be yyyy-mm-dd.',
                'data-validation-format': "yyyy-mm-dd",

            }

            # years=range(1975, 2005)
        )
    )

    mobile = forms.CharField(
        max_length=2500,
        required=False,
        error_messages={'required': 'Please enter the answer.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'maxlength' :"10",
            'data-validation' : "number",
            'data-validation-allowing': "range[1000000000;9999999999]"
        }
        )
    )

    email = forms.CharField(
        required=False,
         max_length=100,
         widget=forms.TextInput(attrs={
             'class': "form-control",
             'data-validation' :"email"
         })
     )


    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if len(data)< 2:
            raise forms.ValidationError("Please Enter more than 2 characters")
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if len(data) < 4:
            raise forms.ValidationError("Please Enter more than 4 characters")
        return data


    def clean_mobile(self):
        value = self.cleaned_data['mobile']

        if not value:
            raise forms.ValidationError('Mobile is required field.')
        else:
            if not User.objects.filter(~Q(id=self.initial.get('pk')), mobile=value).exists():
                # if len(str(value)) != 10:
                #     raise forms.ValidationError('mobile numer should be of 10 digits')
                return value

            else:
                raise forms.ValidationError('Mobile number is already registered.')


    def clean_email(self):
        value = self.cleaned_data['email']

        if not value:
            raise forms.ValidationError('Email is required field.')
        else:
            if not User.objects.filter(~Q(id=self.initial.get('pk')), email=value).exists():
                return value
            else:
                raise forms.ValidationError('This email address already exists.')
        # return value


    def __init__(self, *args, **kwargs):
        super(UpdateClientForm, self).__init__(*args, **kwargs)
