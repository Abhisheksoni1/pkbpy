from django import forms
from apps.stores.models import Kitchen, Store


class CategoryManagementForm(forms.Form):
    STATUS_CHOICE = (('1', "Active"), ('0', "Inactive"))
    name = forms.CharField(
        required=False,
        max_length=100,
        error_messages={'required': 'Please enter Category.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12',
                   'label': 'title',
                   'data-validation': 'required',
                   'data - validation - error - msg': "category is required field",
                   }

        )
    )

    description = forms.CharField(
        max_length=2500,
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
    short_description = forms.CharField(max_length=100,
                                        error_messages={'required': 'Please enter description.'},
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Short Description'
                                                   # 'data-validation': 'required',
                                                   # 'data-validation-error-msg': 'Description is required field',

                                                   }

                                        ))
    status = forms.ChoiceField(

        choices=STATUS_CHOICE,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "btn btn-primary btn-md",
            'data-parsley-multiple': 'gender'
        })
    )

    kitchen = forms.ChoiceField(
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "btn btn-primary btn-md",
            'data-parsley-multiple': 'gender'
        })
    )

    store = forms.ChoiceField(
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "btn btn-primary btn-md stores",
            'data-parsley-multiple': 'gender'
        })
    )

    image = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'type': 'file',
            'data-validation': 'mime',
            'data-validation-allowing': 'jpg, jpeg',
            'data-validation-error-msg-mime': 'You can only upload images in (jpg/jpeg).'
        }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        id = args[1]['store']
        kitchen_id = id
        stores = self.get_store(id)
        bool = True
        if args[1].get('kitchen'):
            kitchen_id = args[1]['kitchen']
            bool = False
        kitchen = self.get_kitchen(kitchen_id, bool)
        self.fields['store'].choices = stores
        self.fields['kitchen'].choices = kitchen

    def get_kitchen(self, id, bool):
        if bool:
            kitchens = Kitchen.objects.filter(store_id=id, is_deleted=False)
        else:
            kitchens = Kitchen.objects.filter(id=id, is_deleted=False)

        kitchen = (tuple((s.pk, s.name) for s in kitchens))
        return kitchen

    def clean_category(self):
        data = self.cleaned_data['category']
        if data is None:
            raise forms.ValidationError('category is required field')
        return data

    def get_store(self, id):
        stores = Store.objects.filter(is_deleted=False, status=True, id=id)
        store = (tuple((s.pk, s.name) for s in stores))
        return store


class UpdateCategory(forms.Form):
    STATUS_CHOICE = (('1', "Active"), ('0', "Inactive"))
    name = forms.CharField(
        required=False,
        max_length=100,
        error_messages={'required': 'Please enter Category.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12',
                   'label': 'title',
                   'data-validation': 'required',
                   'data - validation - error - msg': "category is required field",
                   }

        )
    )

    description = forms.CharField(
        max_length=2500,
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
    short_description = forms.CharField(max_length=100,
                                        error_messages={'required': 'Please enter description.'},
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Short Description'
                                                   # 'data-validation': 'required',
                                                   # 'data-validation-error-msg': 'Description is required field',

                                                   }

                                        ))
    status = forms.ChoiceField(

        choices=STATUS_CHOICE,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        })
    )

    image = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'type': 'file',
            'data-validation': 'mime',
            'data-validation-allowing': 'jpg, jpeg, png',
            'data-validation-error-msg-mime': 'You can only upload images in (jpg/jpeg).'
        }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #     kitchen = self.get_kitchen()
    #     stores = self.get_store()
    #     self.fields['store'].choices = stores
    #     self.fields['kitchen'].choices = kitchen
    #
    # def get_kitchen(self):
    #     kitchens = Kitchen.objects.all()
    #     kitchen = (tuple((s.pk, s.name) for s in kitchens))
    #     return kitchen

    def clean_category(self):
        data = self.cleaned_data['category']
        if data is None:
            raise forms.ValidationError('category is required field')
        return data

    # def get_store(self):
    #     stores = Store.objects.filter(is_deleted=False,status=True)
    #     store = (tuple((s.pk, s.name) for s in stores))
    #     return store
