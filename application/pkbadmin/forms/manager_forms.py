from django import forms
from django.db.models import Q

from apps.users.models import User


class ManagerForm(forms.Form):
    my_default_errors = {
        'required': 'This field is required',
        'invalid': 'Enter a valid value'
    }
    CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    first_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': 'required length',
                'data-validation-length': 'min2',
                'data-validation-error-msg-length': "Please enter minimum 2 characters.",
                'data-validation-error-msg-required': "You did not enter last name.",
                'placeholder': "Enter last name"
            }
    ))

    last_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': 'required length',
                'data-validation-length': 'min2',
                'data-validation-error-msg-length': "Please enter minimum 2 characters.",
                'data-validation-error-msg-required': "You did not enter last name.",
                'placeholder': "Enter last name"
            }
    ))

    gender = forms.CharField(error_messages=my_default_errors)
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
        max_length=10,
        required=False,
        error_messages={'required': 'Please enter the mobile number.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "required number length ",
            'data-validation-length': "min10",
            'data-validation-allowing': "range[1000000000;9999999999]",
            'data-validation-error-msg-required': "You did not enter mobile number",
            'data-validation-error-msg-number': "Please enter a valid mobile number",

        }
        )
    )

    email = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "email",
            'data-validation-error-msg-required': "You did not enter email",
        })
    )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data is None:
            raise forms.ValidationError('First name is required field.')
        if len(data) < 2:
            raise forms.ValidationError("Please Enter more than 2 characters")
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data is None:
            raise forms.ValidationError('Last name is required field')
        if len(data) < 1:
            raise forms.ValidationError("Please Enter the last name.")
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
                        mobile=value, groups__name='Manager').exists():
                    return value
                elif User.objects.filter(mobile=value, groups__name='Manager').exists():
                    raise forms.ValidationError('Moblie number already exist.')

            except Exception as error:
                raise error

    def clean_gender(self):
        value = self.cleaned_data.get('gender')
        gender = ['Male', 'Female', 'Others']
        if not value in gender:
            print(value)
            return forms.ValidationError('gender is required field')
        return value

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
                        email=value, groups__name='Manager').exists():
                    user = User.objects.get(email=value)
                    if user.mobile == mobile:
                        return value
                    else:
                        raise forms.ValidationError('this email id is already exist for user ')
                elif User.objects.filter(email=value, groups__name='Manager').exists():
                    raise forms.ValidationError(' Email id already exists.')
            except Exception as error:
                raise error

    def __init__(self, *args, **kwargs):

        super(ManagerForm, self).__init__(*args, **kwargs)


class ManagerUpdateForm(forms.Form):
    my_default_errors = {
        'required': 'This field is required',
        'invalid': 'Enter a valid value'
    }
    CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    first_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': 'required length',
                'data-validation-length': 'min2',
                'data-validation-error-msg-length': "Please enter minimum 2 characters.",
                'data-validation-error-msg-required': "You did not enter first name.",
                'placeholder': "Enter first name"
            }
    ))

    last_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': 'required length',
                'data-validation-length': 'min2',
                'data-validation-error-msg-length': "Please enter minimum 2 characters.",
                'data-validation-error-msg-required': "You did not enter last name.",
                'placeholder': "Enter last name"
            }
    ))

    gender = forms.CharField(error_messages=my_default_errors)
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
        max_length=10,
        required=False,
        error_messages={'required': 'Please enter the mobile number.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "required number length ",
            'data-validation-length': "min10",
            'data-validation-allowing': "range[1000000000;9999999999]",
            'data-validation-error-msg-required': "You did not enter mobile number",
            'data-validation-error-msg-number': "Please enter a valid mobile number",

        }
        )
    )

    email = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "email",
            'data-validation-error-msg-required': "You did not enter email",
        })
    )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data is None:
            raise forms.ValidationError('first name is required field')
        if len(data) < 2:
            raise forms.ValidationError("Please Enter more than 2 characters")
        return data

    def clean_gender(self):
        data = self.cleaned_data['gender']
        if data:
            return data
        else:
            raise forms.ValidationError("Please choose gender first")

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

    def __init__(self, *args, **kwargs):

        super(ManagerUpdateForm, self).__init__(*args, **kwargs)
