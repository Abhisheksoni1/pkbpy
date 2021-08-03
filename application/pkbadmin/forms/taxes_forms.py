from django import forms


class TaxesForm(forms.Form):
    TAX_CHOICES = [('FORWARD', 'FORWARD'), ('BACKWARD', 'BACKWARD'),
                   ('CALCULATE ON TAX', 'CALCULATE ON TAX')]

    VALUE_CHOICES = [('FIXED', 'FIXED'), ('PERCENTAGE', 'PERCENTAGE')]

    title = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'length',
            'data-validation-length': 'min2',
            'data-validation-error-msg': "You did not enter correct title.",
            'placeholder': "Enter Title"
        })
    )

    tax_type = forms.ChoiceField(
        choices=TAX_CHOICES,
        initial='Forward',
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        })
    )

    value_type = forms.ChoiceField(
        choices=VALUE_CHOICES,
        initial='FIXED',
        widget=forms.Select(attrs={
            'type': 'radio',
            'class': 'form-control',
            'data-parsley-multiple': 'gender'
        })
    )

    description = forms.CharField(
        max_length=100,
        required=False,
        error_messages={'required': 'Please enter the description.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'length',
            'data-validation-length': 'min2',
            'data-validation-error-msg': "You did not enter description",
            'placeholder': "Description"

        })
    )

    amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class': "form-control ",
                                    'data-validation': 'required number length',
                                    'data-validation-length': 'max7',
                                    'data-validation-allowing': "range[1;1000], float",
                                    # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                    'data-validation-error-msg-required': "Please enter the amount.",
                                    'data-validation-error-msg-number': 'Please enter numeric value and should be less than 1000',
                                    'data-validation-error-msg-length': 'Please enter max 5 digit amount',
                                    'placeholder': "Amount",

                                })

                               )
