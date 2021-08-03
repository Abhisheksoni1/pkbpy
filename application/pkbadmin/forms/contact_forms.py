from django import forms
from apps.common.models import ContactPage as Contact


class ContactForm(forms.Form):
    contact_address = forms.CharField(
        max_length=255,
        required=False,
        error_messages={'required': 'Please enter the contact address'},
        widget=forms.TextInput(attrs={'class': "form-control",
                                      'data-validation': "required length",
                                      'data-validation-length': "min10",
                                      'data-validation-error-msg-required': "You did not enter address.",
                                      'data-validation-error-msg-length': "Please enter more than 10 characters.",
                                      'placeholder': 'Contact address'}))

    whatsapp_number = forms.CharField(
        max_length=13,
        required=False,
        error_messages={'required': 'Please enter the whatsapp number.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "required number length ",
            'data-validation-length': "min10",
            'data-validation-allowing': "range[1000000000;9999999999]",
            'data-validation-error-msg-required': "Please enter whatsapp number.",
            'data-validation-error-msg-number': "Input value should be numeric and of 10 digit.",
            'placeholder': "Whatsapp Number"

        }
        )
    )
    paytm_number = forms.CharField(
        max_length=13,
        required=False,
        error_messages={'required': 'Please enter the paytm number.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': "required number length ",
            'data-validation-length': "min10",
            'data-validation-allowing': "range[1000000000;9999999999]",
            'data-validation-error-msg-required': "Please enter paytm number.",
            'data-validation-error-msg-number': "Input value should be numeric and of 10 digit.",
            'placeholder': "Paytm Number"

        }
        )
    )
    email = forms.EmailField(
        required=False,
        error_messages={'required': 'Please enter the email id!'},
        widget=forms.EmailInput(attrs={'class': "form-control",
                                       'data-validation-error-msg': "You did not enter a valid e-mail.",
                                       'placeholder': "Email",
                                       'data-validation': "email"}))

    def clean_contact_address(self):
        data = self.cleaned_data['contact_address']
        data = data.split(' ')
        if len(data)<4:
            raise forms.ValidationError("Please enter more than 4 char.")
        return data




    # will work if we have multiple resturants
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     try:
    #         if not Contact.objects.filter(email=email).exists():
    #             return email
    #         else:
    #             raise forms.ValidationError('Email already exist')
    #     except Exception as e:
    #         raise e
