from django import forms
# from apps.common.models import Page
from apps.stores.models import Kitchen, Store
import magic
# from django.contrib import messages

STATUS_CHOICE = (('0', "Inactive"), ('1', "Active"))


# store_choice = Store.objects.all()

class PromoForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=100,
        error_messages={'required': 'Please enter title.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'maxlength': "30",
                   'data-validation': 'required',
                   'data - validation - error - msg': "Title is required field",
                   }

        )
    )

    description = forms.CharField(max_length=100,
                                  error_messages={'required': 'Please enter description.'},
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control',
                                             'maxlength': "100",
                                             'data-validation': 'required',
                                             'data-validation-error-msg': 'Description is required field',

                                             }

                                  ))
    # print(Store.objects.all())
    store = forms.ChoiceField(
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control stores",
            'data-parsley-multiple': 'gender'
        })
    )
    kitchen = forms.ChoiceField(
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control kitchens",
            'data-parsley-multiple': 'gender'
        })
    )

    banner = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'title': "choose image",
            'type': 'file',
            'data-validation': 'required',
            'data-validation-allowing': 'jpg, jpeg',
            'data-validation-error-msg-mime': 'You can only upload images.'
        }))

    status = forms.ChoiceField(
        initial="1",
        choices=STATUS_CHOICE,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kitchen = self.get_kitchen()
        stores = self.get_store()
        self.fields['store'].choices = stores
        self.fields['kitchen'].choices = kitchen

    def get_store(self):
        store = Store.objects.filter(is_deleted=False, status=True)
        stores = [store for store in store if store.kitchens.all().count() != 0]
        store = (tuple((s.pk, s.name) for s in stores))

        return store

    def clean_title(self):
        data = self.cleaned_data['title']
        if data is None:
            raise forms.ValidationError('Title is required field')
        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        if data is None:
            raise forms.ValidationError('Description is required field')
        return data

    def clean_banner(self):
        file = self.cleaned_data.get("banner")
        file_type = magic.from_buffer(file.read(), mime=True)
        file_split = file_type.split('/')
        extension = file_split[-1]
        types_expected = ["jpeg", "jpg"]
        if not extension in types_expected:
            raise forms.ValidationError('You can only upload images of jpg and jpeg format')
        return file

    def clean_store(self):
        data = self.cleaned_data['store']
        if len(data) == 0:
            raise forms.ValidationError('please add store first to apply banner')
        return data

    def get_kitchen(self):
        kitchens = Kitchen.objects.all()
        kitchen = (tuple((s.pk, s.name) for s in kitchens))
        return kitchen


class PromoEditForm(forms.Form):
    title = forms.CharField(
        required=True,
        max_length=100,
        error_messages={'required': 'Please enter title.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'maxlength': "30",
                   'data-validation': 'required',
                   'data - validation - error - msg': "Title is required field",
                   }

        )
    )

    description = forms.CharField(max_length=100,
                                  error_messages={'required': 'Please enter description.'},
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control',
                                             'data-validation': 'required',
                                             'data-validation-error-msg': 'Description is required field',

                                             }

                                  ))
    # print(Store.objects.all())

    banner = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'title': "choose image",
            'type': "file",
            "data-validation": "mime",
            'data-validation-allowing': "jpg, jpeg",
            'data-validation-error-msg-mime': "You can only upload images."
        })
    )

    status = forms.ChoiceField(

        choices=STATUS_CHOICE,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


