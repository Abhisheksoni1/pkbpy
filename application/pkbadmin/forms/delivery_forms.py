from django import forms
from django.contrib.auth.hashers import make_password
from django.core import signing
from django.db import transaction
from django.utils import timezone

from apps.users.models import User, Group
from django.db.models import Q

from config import settings
from libraries.Email_model import send_auth_email
from libraries.Email_templates import get_manager_registration_verify_content
from libraries.Functions import generate_password
from django.core.validators import validate_email


class DeliveryForm(forms.Form):
    CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    first_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': "30",
            'class': "form-control",
            'data-validation': "required custom",
            'data-validation-regexp': "^([A-Za-z]+[,.]?[ ]?|[A-Za-z]+['-]?)+$",
            'data-validation-error-msg-required': "First name is required field.",
            'data-validation-error-msg-custom': "First name has to be an alphabet."

        })
    )

    last_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': "30",
            'data-validation-length': "max20",
            'class': "form-control",
            'data-validation': "required",
            'data-validation-regexp': "^([A-Za-z]+[,.]?[ ]?|[A-Za-z]+['-]?)+$",
            'data-validation-error-msg-required': "Last name is required field.",
            'data-validation-error-msg': "Last name has to be an alphabet.",
            'data-validation-error-length': "Please enter valid last name."

        })
    )

    gender = forms.ChoiceField(choices=CHOICES,
                               widget=forms.RadioSelect(
                                   attrs={
                                       'data-validation': "required",
                                       'class': "custom-control-input radio",

                                   }
                               )
                               )



    mobile = forms.CharField(
        max_length=20,
        required=False,
        error_messages={'required': 'Please enter the mobile number.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "required number length ",
            'data-validation-length': "min10",
            'data-validation-allowing': "range[1000000000;9999999999]",
            'data-validation-error-msg-required': "Please enter mobile number.",
            'data-validation-error-msg-number': "Input value should be numeric and of 10 digits.",

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

    email = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "email"
        })
    )


    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'mobile', 'dob', 'gender'
        )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data is None:
            raise forms.ValidationError('first name is required field')
        if len(data) < 2:
            raise forms.ValidationError("Please Enter more than 2 characters")
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data is None:
            raise forms.ValidationError('Last name is required field')
        if len(data) < 4:
            raise forms.ValidationError("Please Enter more than 4 characters")
        return data

    def clean_mobile(self):
        value = self.cleaned_data['mobile']

        if not value:
            raise forms.ValidationError('Mobile is required field.')
        else:
            try:
                if not User.objects.filter(mobile=value).exists():
                    if len(str(value)) != 10:
                        raise forms.ValidationError('Mobile number should be of 10 digits.')
                    return value
                elif User.objects.filter(mobile=value, groups__name='User').exists() and not User.objects.filter(
                        mobile=value, groups__name='Delivery boy').exists() and not  User.objects.filter(
                        mobile=value, groups__name='Manager').exists() :
                    return value
                elif User.objects.filter(mobile=value, groups__name='Delivery boy').exists():
                    raise forms.ValidationError('this moblie number is already exist for Delivery boy ')
                elif User.objects.filter(mobile=value, groups__name='Manager').exists():
                    raise forms.ValidationError('this moblie number is already exist for manager ')

            except Exception as error:
                raise error

    def clean_email(self):
        value = self.cleaned_data['email']
        mobile = self.cleaned_data.get('mobile', None)
        if not value:
            raise forms.ValidationError('Email is required field.')
        else:
            try:
                if not User.objects.filter(email=value).exists():
                    return value
                elif User.objects.filter(email=value, groups__name='User').exists() and not User.objects.filter(
                        email=value, groups__name='Delivery boy').exists():
                    user = User.objects.get(email=value)
                    if user.mobile == mobile:
                        return value
                    else:
                        raise forms.ValidationError('This email id is already exist for user ')
                elif User.objects.filter(email=value, groups__name='Delivery boy').exists():
                    raise forms.ValidationError('This email id is already exist for delivery boy ')
            except Exception as error:
                raise error


    #
    # def save(self, commit=True):
    #
    #     instance = super(DeliveryForm, self).save(commit=False)
    #     if self.instance.pk is None:
    #         temp_password = generate_password()
    #         instance.username = self.cleaned_data['email']
    #         instance.name = self.cleaned_data['first_name'] + ' ' + self.cleaned_data['last_name']
    #         instance.first_name = self.cleaned_data['first_name']
    #         instance.last_name = self.cleaned_data['last_name']
    #         instance.email = self.cleaned_data['email']
    #         instance.mobile = self.cleaned_data['mobile']
    #         instance.gender = self.cleaned_data['gender']
    #         instance.password = make_password(temp_password)
    #         instance.is_staff = True
    #         instance.is_superuser = False
    #         instance.is_email_verified = False
    #         instance.created_by = self.initial.get('user')
    #         instance.created_on = timezone.now()
    #         instance.updated_on = timezone.now()
    #     else:
    #         instance.username = self.cleaned_data['email']
    #         instance.first_name = self.cleaned_data['first_name']
    #         instance.last_name = self.cleaned_data['last_name']
    #         instance.email = self.cleaned_data['email']
    #         instance.mobile = self.cleaned_data['mobile']
    #         instance.gender = self.cleaned_data['gender']
    #         instance.updated_on = timezone.now()
    #         instance.save()
    #         return instance
    #
    #     if commit:
    #         with transaction.atomic():
    #             instance.save()
    #             group = Group.objects.get(name='Delivery boy')
    #             group.user_set.add(instance)
    #
    #     if instance:
    #         token_data = {
    #             'id': instance.id,
    #             'email': instance.email
    #         }
    #         token = signing.dumps(token_data)
    #         link = (settings.BASE_URL, '/admin/register-verify/?token=', token)
    #         link = ''.join(link)
    #         data = {
    #             'email': instance.email,
    #             'first_name': instance.first_name,
    #             'last_name': instance.last_name,
    #             'user_name': instance.email,
    #             'password': temp_password,
    #             'link': link
    #         }
    #
    #         body = get_manager_registration_verify_content(data)
    #         receiver = instance.email
    #         subject = "Registration Verification Mail"
    #         send_auth_email.delay(subject, body, receiver)
    #
    #     return instance

    def __init__(self, *args, **kwargs):

        super(DeliveryForm, self).__init__(*args, **kwargs)


class DeliveryUpdateForm(forms.Form):
    CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'maxlength': "30",
            'class': "form-control",
            'data-validation': "required",
            'data-validation-regexp': "^([A-Za-z]+[,.]?[ ]?|[A-Za-z]+['-]?)+$",
            'data-validation-error-msg-required': "First name is required field.",
            'data-validation-error-msg': "First Name has to be an alphabet (max. 30 chars)."

        })
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'maxlength': "30",
            'class': "form-control",
            'data-validation': "required",
            'data-validation-regexp': "^([A-Za-z]+[,.]?[ ]?|[A-Za-z]+['-]?)+$",
            'data-validation-error-msg-required': "Last name is required field.",
            'data-validation-error-msg': "Last Name has to be an alphabet (max. 30 chars)."

        })
    )

    gender = forms.ChoiceField(choices=CHOICES,
                               widget=forms.RadioSelect(
                                   attrs={'data-validation': "required",
                                          'class': "custom-control-input radio",
                                          'data-validation-error-msg': "Gender is required field."
                                          }
                               ))



    mobile = forms.CharField(
        max_length=2500,
        required=False,
        error_messages={'required': 'Please enter the answer.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'maxlength': "10",
            'data-validation': "number",
            'data-validation-allowing': "range[1000000000;9999999999]"
        }
        ))
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

    email = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "email"
        }))



    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data is None:
            raise forms.ValidationError('first name is required field')
        if len(data) < 2:
            raise forms.ValidationError("Please Enter more than 2 characters")
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data is None:
            raise forms.ValidationError('Last name is required field')
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
                raise forms.ValidationError('Please enter valid email address.')
        # return value


    # def save(self, commit=True):
    #     if commit:
    #         with transaction.atomic():
    #             instance = User.objects.filter(id=self.initial.get('pk')). \
    #                 update(username=self.cleaned_data['email'],
    #                        first_name=self.cleaned_data['first_name'],
    #                        last_name=self.cleaned_data['last_name'],
    #                        name=self.cleaned_data['first_name'] + ' ' + self.cleaned_data['last_name'],
    #                        email=self.cleaned_data['email'],
    #                        mobile=self.cleaned_data['mobile'],
    #                        gender=self.cleaned_data['gender'],
    #                        updated_on=timezone.now())
    #     return instance

    def __init__(self, *args, **kwargs):
        super(DeliveryUpdateForm, self).__init__(*args, **kwargs)
