from django import forms
from django.contrib.gis.geos import Point
from apps.stores.models import Kitchen, Store


class KitchenForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required',
            'data-validation-length': 'min2',
            'data-validation-error-msg-required': "You did not enter kitchen name.",
            'data-validation-error-msg-length': "You did not enter kitchen name.",
            'placeholder': " Kitchen Name."
        })
    )
    short_name = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required',
            'data-validation-length': 'min2',
            'data-validation-error-msg-required': "You did not enter short name.",
            'data-validation-error-msg-length': "Length of short name should be grater than 2",
            'placeholder': " Kitchen short Name."
        })
    )

    tag_line = forms.CharField(
        max_length=100,
        required=False,
        error_messages={'required': 'Please enter the tag line.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            # 'data-validation': 'length',
            'data-validation-length': 'max20',
            # 'data-validation-error-msg': "You did not enter tag line.",
            'placeholder': "Tag Line"

        })
    )

    logo = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'type': "file",
            "data-validation": "mime",
            'data-validation-allowing': "jpg, jpeg",
            'data-validation-error-msg-mime': "You can only upload images in (jpg/jpeg)."
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

            'data-validation-error-msg-required': "You did not enter longitude value.",
            'data-validation-error-msg': "Please Enter Longitude value.",
            'id': 'lngbox'

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
            'data-validation-error-msg-required': "You did not enter latitude.",
            'data-validation-error-msg': "Please Enter Latitude value.",
            'id': 'latbox'
        })
    )

    address = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control address",
            'data-validation': 'length',
            'data-validation-length': 'min4',
            'data-validation-error-msg-required': "You did not enter address.",
            # 'data-validation-error-msg': "Please enter the address or drag the marker on correct location",
            'data-validation-error-msg-length': "You did not enter address.",
            'placeholder': "Address"
        })
    )

    store = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': "form-control",
        })
    )

    opening_time = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control time',
                                       # 'data-validation': "time",
                                       'data-validation': 'required length',
                                       # 'data-validation-help': "HH:mm",
                                       'data-validation-length': 'max20',
                                       'data-validation-error-msg-required': "You did not enter opening time.",
                                       'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS',
                                       'placeholder': "Opening Time"
                                   }
                                   )
                                   )
    closing_time = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control time',
                                       'data-validation': 'required length',
                                       'data-validation-length': 'max20',
                                       'data-validation-error-msg-required': "You did not enter closing time.",
                                       'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS',
                                       'placeholder': "Closing Time"
                                   }
                                   )
                                   )

    location = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )


    cost_for_two = forms.DecimalField(max_digits=7, decimal_places=2,
                       required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-allowing': "float",
            'data-validation-length': 'max7',
            'data-validation-error-msg-required': "You did not enter the cost for two.",
            'data-validation-error-msg-number': "Please enter numeric values.",
            'placeholder': "Cost for Two"

        })
    )

    minimum_order = forms.DecimalField(max_digits=7, decimal_places=2,
                       required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-length': 'max7',
            'data-validation-allowing': "float",
            'data-validation-error-msg-required': "You did not enter the minimum order.",
            'data-validation-error-msg-number': "Please enter numeric values.",
            'placeholder': "Minimum Order"

        })
    )

    delivery_time = forms.DecimalField(max_digits=7, decimal_places=2,
                       required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-length': 'max7',
            'data-validation-allowing': "float",
            'data-validation-error-msg-required': "You did not enter the minimum order.",
            'data-validation-error-msg-number': "Please enter numeric values.",
            'placeholder': "Minimum Order"

        })
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
            'data-validation-error-msg-required': "You did not enter mobile number.",
            'data-validation-error-msg-number': "Please enter a valid mobile number",
            'placeholder': "Mobile Number"

        }
        )
    )
    delivery_charges = forms.DecimalField(max_digits=7, decimal_places=2,
                       required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-length': 'max7',
            'data-validation-allowing': "float",
            'data-validation-error-msg-required': "You did not enter the delivery charges.",
            'data-validation-error-msg-number': "Please enter numeric values.",
            'placeholder': "Delivery Charges"

        })
    )
    packing_charges = forms.DecimalField(max_digits=7, decimal_places=2,
                       required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-length': 'max7',
            'data-validation-allowing': "float",
            'data-validation-error-msg-required': "You did not enter the packing charges.",
            'data-validation-error-msg-number': "Please enter numeric values.",
            'placeholder': "Delivery Charges"

        })
    )
    cod_limit = forms.DecimalField(max_digits=7, decimal_places=2,
                       required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "cod limit value"

        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        id = args[1]['store']
        stores = self.get_store(id)

        self.fields['store'].choices = stores


    def clean_cod_limit(self):
        cod = self.cleaned_data['cod_limit']
        print(type(cod))
        return cod

    def clean_longitude(self):
        try:
            long = self.cleaned_data['longitude']
            if long == '':
                return long
            long = float(long)
            if not isinstance(long, float):
                raise forms.ValidationError("Please enter the valid value.")
            return long
        except ValueError:
            raise forms.ValidationError("Something went wrong please try again.!!")

    def clean_latitude(self):
        try:
            lat = self.cleaned_data['latitude']
            if lat == '':
                return lat
            lat = float(lat)
            if not isinstance(lat, float):
                raise forms.ValidationError("Please enter the valid value.")
            return lat
        except ValueError:
            raise forms.ValidationError("Something went wrong please try again.!!")

    def get_store(self,id):
        store = Store.objects.filter(id=id)
        stores = (tuple((s.pk, s.name)) for s in store)
        return stores

    def clean_location(self):
        data = self.cleaned_data['location']
        try:
            df = data.split(',')
            point = Point(x=float(df[0]), y=float(df[1]))
            return point
        except:
            return data

    def clean_name(self):
        data = self.cleaned_data['name']
        # store = int(self.store_id)
        # kitchens = Kitchen.objects.filter(store_id=self.store_id).values_list('name', flat=True)
        if data is None:
            raise forms.ValidationError("Please enter kitchen name.")

        return data

    def clean_address(self):
        data = self.cleaned_data['address']
        if data is None:
            raise forms.ValidationError("Please enter address.")
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


class UpdateKitchenForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required',
            'data-validation-length': 'min2',
            'data-validation-error-msg-required': "You did not enter kitchen name.",
            'data-validation-error-msg-length': "You did not enter kitchen name.",
            'placeholder': " Kitchen Name."
        })
    )
    short_name = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required',
            'data-validation-length': 'min2',
            'data-validation-error-msg-required': "You did not enter short name.",
            'data-validation-error-msg-length': "Length of short name should be grater than 2",
            'placeholder': " Kitchen short Name."
        })
    )

    tag_line = forms.CharField(
        max_length=100,
        required=False,
        error_messages={'required': 'Please enter the tag line.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            # 'data-validation': 'length',
            'data-validation-length': 'max20',
            # 'data-validation-error-msg': "You did not enter tag line.",
            'placeholder': "Tag Line"

        })
    )

    logo = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'type': "file",
            "data-validation": "mime",
            'data-validation-allowing': "jpg, jpeg",
            'data-validation-error-msg-mime': "You can only upload images in (jpg/jpeg)."
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

            'data-validation-error-msg-required': "You did not enter longitude value.",
            'data-validation-error-msg': "Please Enter Longitude value.",
            'id': 'lngbox'

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
            'data-validation-error-msg-required': "You did not enter latitude.",
            'data-validation-error-msg': "Please Enter Latitude value.",
            'id': 'latbox'
        })
    )

    address = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control address",
            'data-validation': 'length',
            'data-validation-length': 'min4',
            'data-validation-error-msg-required': "You did not enter address.",
            # 'data-validation-error-msg': "Please enter the address or drag the marker on correct location",
            'data-validation-error-msg-length': "You did not enter address.",
            'placeholder': "Address"
        })
    )


    opening_time = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control time',
                                       # 'data-validation': "time",
                                       'data-validation': 'required length',
                                       # 'data-validation-help': "HH:mm",
                                       'data-validation-length': 'max20',
                                       'data-validation-error-msg-required': "You did not enter opening time.",
                                       'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS',
                                       'placeholder': "Opening Time"
                                   }
                                   )
                                   )
    closing_time = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control time',
                                       'data-validation': 'required length',
                                       'data-validation-length': 'max20',
                                       'data-validation-error-msg-required': "You did not enter closing time.",
                                       'data-validation-error-msg': 'Time is required field and format should be HH:MM:SS',
                                       'placeholder': "Closing Time"
                                   }
                                   )
                                   )

    location = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    cost_for_two = forms.DecimalField(max_digits=7, decimal_places=2,
                                      required=False,
                                      widget=forms.TextInput(attrs={
                                          'class': "form-control",
                                          'data-validation': 'required number',
                                          'data-validation-allowing': "float",
                                          'data-validation-length': 'max7',
                                          'data-validation-error-msg-required': "You did not enter the cost for two.",
                                          'data-validation-error-msg-number': "Please enter numeric values.",
                                          'placeholder': "Cost for Two"

                                      })
                                      )

    minimum_order = forms.DecimalField(max_digits=7, decimal_places=2,
                                       required=False,
                                       widget=forms.TextInput(attrs={
                                           'class': "form-control",
                                           'data-validation': 'required number',
                                           'data-validation-length': 'max7',
                                           'data-validation-allowing': "float",
                                           'data-validation-error-msg-required': "You did not enter the minimum order.",
                                           'data-validation-error-msg-number': "Please enter numeric values.",
                                           'placeholder': "Minimum Order"

                                       })
                                       )

    delivery_time = forms.DecimalField(max_digits=7, decimal_places=2,
                       required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-length': 'max7',
            'data-validation-allowing': "float",
            'data-validation-error-msg-required': "You did not enter the minimum order.",
            'data-validation-error-msg-number': "Please enter numeric values.",
            'placeholder': "Minimum Order"

        })
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
            'data-validation-error-msg-required': "You did not enter mobile number.",
            'data-validation-error-msg-number': "Please enter a valid mobile number",
            'placeholder': "Mobile Number"

        }
        )
    )
    delivery_charges = forms.DecimalField(max_digits=7, decimal_places=2,
                                          required=False,
                                          widget=forms.TextInput(attrs={
                                              'class': "form-control",
                                              'data-validation': 'required number',
                                              'data-validation-length': 'max7',
                                              'data-validation-allowing': "float",
                                              'data-validation-error-msg-required': "You did not enter the delivery charges.",
                                              'data-validation-error-msg-number': "Please enter numeric values.",
                                              'placeholder': "Delivery Charges"

                                          })
                                          )
    packing_charges = forms.DecimalField(max_digits=7, decimal_places=2,
                                         required=False,
                                         widget=forms.TextInput(attrs={
                                             'class': "form-control",
                                             'data-validation': 'required number',
                                             'data-validation-length': 'max7',
                                             'data-validation-allowing': "float",
                                             'data-validation-error-msg-required': "You did not enter the packing charges.",
                                             'data-validation-error-msg-number': "Please enter numeric values.",
                                             'placeholder': "Packing Charges"

                                         })
                                         )
    cod_limit = forms.DecimalField(max_digits=7, decimal_places=2,
                                   required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': "form-control",
                                       'placeholder': "cod limit value"

                                   })
                                   )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # stores = self.get_store()
        # self.fields['store'].choices = stores

        # print(stores)

    def clean_longitude(self):
        try:
            long = self.cleaned_data['longitude']
            if long == '':
                return long
            long = float(long)
            if not isinstance(long, float):
                raise forms.ValidationError("Please enter the valid value.")
            return long
        except ValueError:
            raise forms.ValidationError("Something went wrong please try again.!!")

    def clean_latitude(self):
        try:
            lat = self.cleaned_data['latitude']
            if lat == '':
                return lat
            lat = float(lat)
            if not isinstance(lat, float):
                raise forms.ValidationError("Please enter the valid value.")
            return lat
        except ValueError:
            raise forms.ValidationError("Something went wrong please try again.!!")

    # def get_store(self):
    #     stores = Store.objects.all()
    #     store = (tuple((s.pk, s.name) for s in stores))
    #     return store

    def clean_location(self):
        data = self.cleaned_data['location']
        try:
            df = data.split(',')
            point = Point(x=float(df[0]), y=float(df[1]))
            return point
        except:
            return data

    def clean_name(self):
        data = self.cleaned_data['name']
        # store = int(self.store_id)
        # kitchens = Kitchen.objects.filter(store_id=self.store_id).values_list('name', flat=True)
        if data is None:
            raise forms.ValidationError("Please enter kitchen name.")

        return data

    def clean_address(self):
        data = self.cleaned_data['address']
        if data is None:
            raise forms.ValidationError("Please enter address.")
        return data

    def clean_location(self):
        try:
            point = Point(x=float(self.cleaned_data['longitude']), y=float(self.cleaned_data['latitude']))
            return point
        except:
            pass

    def clean_cod_limit(self):
        cod = self.cleaned_data['cod_limit']
        if cod:
            try:
                cod = float(cod)
            except Exception:
                raise forms.ValidationError('cod_limit should be float value')
        return cod
    def clean_closing_time(self):
        opening_time= self.cleaned_data['opening_time']
        closing_time = self.cleaned_data['closing_time']
        if closing_time<opening_time:
            raise forms.ValidationError('Closing time should be greater than opening time')
        return closing_time