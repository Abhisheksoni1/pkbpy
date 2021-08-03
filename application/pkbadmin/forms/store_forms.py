from django import forms
from django.contrib.gis.geos import Point
from apps.stores.models import Store
from apps.users.models import User, Group


class StoreForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        error_messages={'required': 'Please enter the store name.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'length',
            'data-validation-length': 'min2',
            'data-validation-error-msg': "You did not enter correct store name.",
            'placeholder': "Enter Store Name"
        })
    )

    tag_line = forms.CharField(
        max_length=25,
        required=False,
        error_messages={'required': 'Please enter the tag line.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            # 'data-validation': 'length',
            # 'data-validation-length': 'min2',
            # 'data-validation-error-msg': "You did not enter tag line.",
            'placeholder': "Tag Line"

        })
    )

    logo = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'type': "file",
            "data-validation": "mime",
            "data-validation-allowing": "jpg, jpeg",
            "data-validation-error-msg-mime": "You can only upload images in (jpg/jpeg)."
        })
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

    description = forms.CharField(
        max_length=100,
        required=False,
        error_messages={'required': 'Please enter the answer.'},
        widget=forms.Textarea(attrs={
            'class': "form-control",
            # 'data-validation': 'length',
            # 'data-validation-length': 'min2',
            # 'data-validation-error-msg': "You did not enter the description.",
            'placeholder': "Description"
        }
        )
    )

    longitude = forms.CharField(
        required=False,
        max_length=100,
        error_messages={'required': 'Please enter the longitude.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': 'Longitude',
            'data-validation': 'number',
            'data-validation-allowing': 'float',
            'id': 'lngbox',
            'data-validation-error-msg': "Please Enter Longitude detail."
        })
    )

    latitude = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': 'Latitude',
            'data-validation': 'number',
            'data-validation-allowing': 'float',
            'id': 'latbox',
            'data-validation-error-msg': "Please Enter Latitude detail."
        })
    )
    address = forms.CharField(
        max_length=100,
        required=False,
        error_messages={'required': 'Please enter  address.'},
        widget=forms.TextInput(attrs={
            'class': "form-control address",
            'data-validation': 'length',
            'data-validation-length': 'min4',
            'data-validation-error-msg': "You did not enter address.",
            'placeholder': "Address"
        })
    )

    tin_no = forms.CharField(
        max_length=20,
        required=False,
        error_messages={'required': 'Please enter the store name.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'length',
            'data-validation-length': 'min4',
            'data-validation-error-msg': "Please enter valid TIN no.",
            'placeholder': "Enter TIN No"
        })
    )

    location = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    # manager = forms.ChoiceField(
    #     widget=forms.Select(attrs={
    #         'type': "radio",
    #         'class': "btn btn-primary btn-md",
    #     })
    #     )
    opening_time = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control time',
                                       'data-validation': 'required length',
                                       'data-validation-length': 'max20',
                                       'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS',
                                       'placeholder': "Opening time"
                                   }
                                   )
                                   )
    closing_time = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control time',
                                        'data-validation': 'required length',
                                       'data-validation-length': 'max20',
                                       'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS',
                                       'placeholder': "Closing time"
                                   }
                                   )
                                   )
    cost_for_two = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-allowing': "float",
            'data-validation-length': 'max5',
            'data-validation-error-msg-required': "You did not enter the price.",
            'data-validation-error-msg-number': "Please enter numeric values.",
            'placeholder': "Cost for Two"

        })
    )

    minimum_order = forms.CharField(
        max_length=7,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-length': 'max7',
            'data-validation-allowing': "float",
            'data-validation-error-msg-required': "You did not enter the price.",
            'data-validation-error-msg-number': "Please enter numeric values.",
            'placeholder': "Minimum Order"

        })
    )

    delivery_time = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-allowing': "float",
            'data-validation-length': 'max5',
            'data-validation-error-msg-required': "You did not enter the delivery time(in minutes).",
            'data-validation-error-msg-number': "Please enter numeric value in minutes.",
            'placeholder': "Delivery time"

        })
    )

    def clean_longitude(self):
        try:
            long = self.cleaned_data['longitude']
            if long == '':
                return long
            long = float(long)
            if not isinstance(long, float):
                raise forms.ValidationError("Please enter the valid Longitude detail.")
            return long
        except ValueError:
            raise forms.ValidationError("Please enter the valid Longitude detail.")

    def clean_latitude(self):
        try:
            lat = self.cleaned_data['latitude']
            if lat == '':
                return lat
            lat = float(lat)
            if not isinstance(lat, float):
                raise forms.ValidationError("Please enter the valid Latitude detail.")
            return lat
        except ValueError:
            raise forms.ValidationError("Please enter the valid Latitude detail.")

    def clean_name(self):
        data = self.cleaned_data['name']
        if data is None:
            raise forms.ValidationError("Please enter  valid Store name.")
        return data

    def clean_address(self):
        data = self.cleaned_data['address']
        if data is None:
            raise forms.ValidationError("Please enter address.")
        return data

    def clean_tin_no(self):
        data = self.cleaned_data['tin_no']
        if data is None:
            raise forms.ValidationError("Please enter tin no.")
        return data

    def clean_location(self):
        try:
            point = Point(x=float(self.cleaned_data['longitude']), y=float(self.cleaned_data['latitude']))
            return point
        except:
            pass
    def clean_closing_time(self):
        opening_time= self.cleaned_data['opening_time']
        closing_time = self.cleaned_data['closing_time']
        if closing_time<opening_time:
            raise forms.ValidationError('Closing time should be greater than opening time')
        return closing_time

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
