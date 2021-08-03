from django import forms
from apps.users.models import User, Group
from apps.discounts.models import PromoCode
from datetime import date
from django.db.models import Q
TYPE_CHOICES = [('Percentage', 'Percentage'),
                ('Fixed', 'Fixed')]
STATUS_CHOICE = ((False, "Inactive"), (True, "Active"))


class PromoCodeForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=50,
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

    image = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'type': "file",
            "data-validation": "mime",
            'data-validation-allowing': "jpg, jpeg",
            'data-validation-error-msg-mime': "You can only upload images in (jpg/jpeg)."
        })
    )

    type = forms.ChoiceField(choices=TYPE_CHOICES,
                             required=False,
                             widget=forms.Select(attrs={
                                 'type': "radio",
                                 'class': "form-control",
                                 'data-parsley-multiple': 'gender'
                             })
                             )

    description = forms.CharField(max_length=100,
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control',
                                             'label': 'title',
                                             'data-validation': 'required',
                                             'data-validation-error-msg': "Description is required field.",
                                             'placeholder': 'Description'
                                             }
                                  ))
    max_discount = forms.DecimalField(max_digits=7, decimal_places=2,
                                      required=False,
                                      widget=forms.TextInput(attrs={
                                          'class': 'form-control',
                                          'data-validation-length': 'max7',
                                          'data-validation-allowing': "range[1;1000], float",
                                          # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                          'data-validation-error-msg-required': "Please enter the amount.",
                                          'data-validation-error-msg-number': 'Please enter numeric value and should be less than 1000.',
                                          'data-validation-error-msg-length': 'Please enter max 5 digit amount.',
                                          'placeholder': "Maximum discount.",
                                      })
                                      )
    amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'data-validation-length': 'max7',
                                    'data-validation-allowing': "range[1;10000], float",
                                    # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                    'data-validation-error-msg-required': "Please enter the amount.",
                                    'data-validation-error-msg-number': 'Please enter numeric value and should be less than 10000.',
                                    'data-validation-error-msg-length': 'Please enter max 5 digit amount',
                                    'placeholder': "Amount",

                                })
                                )
    percentage = forms.DecimalField(max_digits=7, decimal_places=2,
                                    required=False,
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'data-validation-length': 'max7',
                                        'data-validation-allowing': "range[1;10000], float",
                                        # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                        'data-validation-error-msg-required': "Please enter the amopercentageunt.",
                                        'data-validation-error-msg-number': 'Please enter numeric value and should be less than 10000.',
                                        'data-validation-error-msg-length': 'Please enter max 5 digit amount',
                                        'placeholder': "Percentage",

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
                'data-validation-error-msg': 'Date is required field and format should be yyyy-mm-dd.',
                'data-validation-format': "yyyy-mm-dd",

            }

            # years=range(1975, 2005)
        )
    )
    to_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control to',
                # 'data-validation-error-msg-container': "#txtFromDate",
                'data-validation': "date",
                'data - validation - require - leading - zero': "false",
                'data-validation-error-msg': 'Date is required field and format should be yyyy-mm-dd.',
                'data-validation-format': "yyyy-mm-dd",

            }))
    from_time = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control time',
                                    'data-validation': 'required length',
                                    # 'data-validation-help': "HH:mm",
                                    'data-validation-length': 'max20',
                                    'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS.',
                                }
                                )
                                )

    to_time = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control time',
                                  'data-validation': 'required length',
                                  # 'data-validation-help': "HH:mm",
                                  'data-validation-length': 'max20',
                                  'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS.',
                              }
                              )
                              )
    minimum_order = forms.DecimalField(max_digits=7, decimal_places=2,
                                       required=False,
                                       widget=forms.TextInput(attrs={
                                           'class': 'form-control',
                                           'data-validation-length': 'max7',
                                           'data-validation-allowing': "range[1;10000], float",
                                           # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                           'data-validation-error-msg-required': "Please enter the amount.",
                                           'data-validation-error-msg-number': 'Please enter numeric value and should be less than 10000.',
                                           'data-validation-error-msg-length': 'Please enter max 5 digit amount',
                                           'placeholder': "Minimum order",

                                       })
                                       )
    code = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control code",
                   'label': 'code',
                   'data - validation - error - msg': "code is required field",
                   # 'placeholder': "Code"
                   }

        ))

    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        from_date = self.cleaned_data['from_date']
        toDate = date(*map(int, to_date.split('-')))
        fromDate = date(*map(int, from_date.split('-')))
        if toDate.year == fromDate.year:
            if toDate.month == fromDate.month:
                if toDate.day < fromDate.day:
                    raise forms.ValidationError('to date day should be grater then from date')
            elif toDate.month < fromDate.month:
                raise forms.ValidationError('to date month should be grater then from date')
        if toDate.year < fromDate.year:
            raise forms.ValidationError('to date year should be grater then from date')
        return to_date

    def clean_code(self):
        code = self.cleaned_data['code']
        if PromoCode.objects.filter(code__iexact=code, is_deleted=False).exists():
            raise forms.ValidationError('this code already exists')
        else:
            return code

    # class UserPromoCodeForm(forms.Form):
    #     user = forms.ChoiceField(
    #         widget=forms.Select(attrs={
    #             'class': "btn btn-primary btn-md",
    #         })
    #     )
    #     promo = forms.ChoiceField(
    #         widget=forms.Select(attrs={
    #             'class': "btn btn-primary btn-md",
    #         })
    #     )
    #
    #     def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #
    #         users = self.get_user()
    #         promo = self.get_promo()
    #         self.fields['user'].choices = users
    #         self.fields['promo'].choices = promo
    #
    #     def get_user(self):
    #         users = User.objects.all()
    #         user = (tuple((s.pk, s.name) for s in users))
    #         return user
    #
    #     def get_promo(self):
    #         promo = PromoCode.objects.filter(is_deleted=False)
    #         promo = (tuple((s.pk, s.name) for s in promo))
    #         return promo



class UpdatePromoCodeForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=50,
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

    image = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'type': "file",
            "data-validation": "mime",
            'data-validation-allowing': "jpg, jpeg",
            'data-validation-error-msg-mime': "You can only upload images in (jpg/jpeg)."
        })
    )

    type = forms.ChoiceField(choices=TYPE_CHOICES,
                             required=False,
                             widget=forms.Select(attrs={
                                 'type': "radio",
                                 'class': "form-control",
                                 'data-parsley-multiple': 'gender'
                             })
                             )

    description = forms.CharField(max_length=100,
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control',
                                             'label': 'title',
                                             'data-validation': 'required',
                                             'data-validation-error-msg': "Description is required field.",
                                             'placeholder': 'Description'
                                             }
                                  ))
    max_discount = forms.DecimalField(max_digits=7, decimal_places=2,
                                      required=False,
                                      widget=forms.TextInput(attrs={
                                          'class': 'form-control',
                                          'data-validation-length': 'max7',
                                          'data-validation-allowing': "range[1;1000], float",
                                          # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                          'data-validation-error-msg-required': "Please enter the amount.",
                                          'data-validation-error-msg-number': 'Please enter numeric value and should be less than 1000.',
                                          'data-validation-error-msg-length': 'Please enter max 5 digit amount.',
                                          'placeholder': "Maximum discount.",
                                      })
                                      )
    amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'data-validation-length': 'max7',
                                    'data-validation-allowing': "range[1;10000], float",
                                    # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                    'data-validation-error-msg-required': "Please enter the amount.",
                                    'data-validation-error-msg-number': 'Please enter numeric value and should be less than 10000.',
                                    'data-validation-error-msg-length': 'Please enter max 5 digit amount',
                                    'placeholder': "Amount",

                                })
                                )
    percentage = forms.DecimalField(max_digits=7, decimal_places=2,
                                    required=False,
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'data-validation-length': 'max7',
                                        'data-validation-allowing': "range[1;10000], float",
                                        # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                        'data-validation-error-msg-required': "Please enter the amopercentageunt.",
                                        'data-validation-error-msg-number': 'Please enter numeric value and should be less than 10000.',
                                        'data-validation-error-msg-length': 'Please enter max 5 digit amount',
                                        'placeholder': "Percentage",

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
                'data-validation-error-msg': 'Date is required field and format should be yyyy-mm-dd.',
                'data-validation-format': "yyyy-mm-dd",

            }

            # years=range(1975, 2005)
        )
    )
    to_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control to',
                # 'data-validation-error-msg-container': "#txtFromDate",
                'data-validation': "date",
                'data - validation - require - leading - zero': "false",
                'data-validation-error-msg': 'Date is required field and format should be yyyy-mm-dd.',
                'data-validation-format': "yyyy-mm-dd",

            }))
    from_time = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control time',
                                    'data-validation': 'required length',
                                    # 'data-validation-help': "HH:mm",
                                    'data-validation-length': 'max20',
                                    'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS.',
                                }
                                )
                                )

    to_time = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control time',
                                  'data-validation': 'required length',
                                  # 'data-validation-help': "HH:mm",
                                  'data-validation-length': 'max20',
                                  'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS.',
                              }
                              )
                              )
    minimum_order = forms.DecimalField(max_digits=7, decimal_places=2,
                                       required=False,
                                       widget=forms.TextInput(attrs={
                                           'class': 'form-control',
                                           'data-validation-length': 'max7',
                                           'data-validation-allowing': "range[1;10000], float",
                                           # 'data-validation-help': 'enter float value  which contain max 7 digit ',
                                           'data-validation-error-msg-required': "Please enter the amount.",
                                           'data-validation-error-msg-number': 'Please enter numeric value and should be less than 10000.',
                                           'data-validation-error-msg-length': 'Please enter max 5 digit amount',
                                           'placeholder': "Minimum order",

                                       })
                                       )
    code = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control code",
                   'label': 'code',
                   'data - validation - error - msg': "code is required field",
                   # 'placeholder': "Code"
                   }

        ))

    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        from_date = self.cleaned_data['from_date']
        toDate = date(*map(int, to_date.split('-')))
        fromDate = date(*map(int, from_date.split('-')))
        if toDate.year == fromDate.year:
            if toDate.month == fromDate.month:
                if toDate.day < fromDate.day:
                    raise forms.ValidationError('to date day should be grater then from date')
            elif toDate.month < fromDate.month:
                raise forms.ValidationError('to date month should be grater then from date')
        if toDate.year < fromDate.year:
            raise forms.ValidationError('to date year should be grater then from date')
        return to_date

    def clean_code(self):
        code = self.cleaned_data['code']
        print(PromoCode.objects.filter(~Q(id=self.initial.get('pk')), code__exact=code, is_deleted=False))
        print(self.initial.get('pk'))
        print(PromoCode.objects.filter(code__exact=code))
        if PromoCode.objects.filter(~Q(id=self.initial.get('pk')),code__exact=code,is_deleted = False).exists():
            raise forms.ValidationError('this code already exists')
        else:
            return code