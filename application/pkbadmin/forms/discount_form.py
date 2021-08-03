from django import forms

TYPE_CHOICES = [('Percentage', 'Percentage'),
                ]
# ('Fixed', 'Fixed')
DISCOUNT_CHOICE = [('Desktop', 'Desktop'),
                   ('Online', 'Online')]
VALIDATE_CHOICES = [(False, 'False'), (True, 'True')]
STATUS_CHOICE = ((False, "Inactive"), (True, "Active"))

ADD_CHOICES = (('ADD_ON_CORE', 'CORE'),
               ('ADD_ON_TOTAL', 'TOTAL'),
               )


class DiscountForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'data-validation': 'required length',
                'data-validation-length': 'min2',
                'data-validation-error-msg-length': "Please enter minimum 2 characters.",
                'data-validation-error-msg-required': "Please enter title.",
                'placeholder': "Enter Title"
            }

        )
    )

    type = forms.ChoiceField(choices=TYPE_CHOICES,
                             required=False,
                             widget=forms.Select(attrs={
                                 'type': "radio",
                                 'class': "form-control",
                                 'data-parsley-multiple': 'gender'
                             })
                             )

    description = forms.CharField(max_length=50,
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control',
                                             'label': 'title',
                                             'data-validation': 'required',
                                             'data-validation-error-msg': "Description is required field.",
                                             }
                                  ))
    terms_and_conditions = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'data-validation': 'required',
            'data-validation-error-msg': 'Terms and Conditions is required field.'
        }
        )
    )

    percentage = forms.DecimalField(max_digits=7, decimal_places=2,
                                      required=False,
                                      widget=forms.TextInput(attrs={
                                          'class': 'form-control',
                                          'data-validation-length': 'max7',
                                          'data-validation': 'number length',
                                          'data-validation-allowing': "range[1;100], float",
                                          # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                          'data-validation-error-msg-required': "Please enter the amount.",
                                          'data-validation-error-msg-number': 'Please enter valid percentage within range(1,100).',
                                          'data-validation-error-msg-length': 'Please enter max 5 digit amount.',
                                          'placeholder': " discount-percentage.",
                                      })
                                      )

    validate_on_code = forms.ChoiceField(choices=VALIDATE_CHOICES,
                                         initial=True,
                                         widget=forms.Select(attrs={
                                             'type': "radio",
                                             'class': "form-control",
                                             'data-parsley-multiple': 'gender'
                                         })
                                         )

    status = forms.ChoiceField(

        choices=STATUS_CHOICE,
        initial=True,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        }))

    from_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datepicker',
                # 'data-validation-error-msg-container': "#txtFromDate",
                'data-validation': "date",
                'data-validation-require-leading-zero': "false",
                'data-validation-error-msg': 'Date is required field.',
                'data-validation-format': "yyyy-mm-dd",

            }

            # years=range(1975, 2005)
        )
    )
    to_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datepicker',
                # 'data-validation-error-msg-container': "#txtFromDate",

                'data-validation': "date",
                'data - validation - require - leading - zero': "false",
                'data-validation-error-msg': 'Date is required field.',
                'data-validation-format': "yyyy-mm-dd",

            }))

    amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'data-validation-length': 'max7',
                                    'data-validation-allowing': "range[1;10000], float",
                                    'data-validation': 'required number length',
                                    'data-validation-error-msg-required': "Please enter the amount.",
                                    'data-validation-error-msg-number': 'Please enter numeric value and should be less than 10000.',
                                    'data-validation-error-msg-length': 'Please enter max 5 digit amount',
                                    'placeholder': "Amount",

                                })
                                )

    from_time = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control time',
                                    'data-validation': 'required length',
                                    'data-validation-length': 'max20',
                                    # 'data-validation-format': "HH:MM",
                                    'data-validation-error-msg': 'Time is required field.',
                                }
                                )
                                )

    to_time = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control time',
                                  'data-validation': 'required length',
                                  # 'data-validation-format': "HH:MM",
                                  'data-validation-length': 'max20',
                                  'data-validation-error-msg': 'Time is required field.',
                              }
                              )
                              )
    code = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(
            attrs={'class': "form-control code",
                   'label': 'code',
                   'data - validation - error - msg': "code is required field",
                   # 'placeholder': "Code"
                   }

        ))

    add_on = forms.ChoiceField(

        choices=ADD_CHOICES,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        })
    )

    order_type = forms.CharField()

    def clean_to_date(self):
        start_date = self.cleaned_data['from_date']
        end_date = self.cleaned_data['to_date']
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")
        return end_date
