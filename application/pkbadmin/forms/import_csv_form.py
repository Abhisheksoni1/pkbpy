from django import forms
from apps.stores.models import Kitchen, Store


class CsvImportForm(forms.Form):
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
            'class': "form-control  stores",
            'data-parsley-multiple': 'gender'
        })
    )
    csv_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'type': "file",
            'class': "csv",
            "data-validation": "mime",
            'data-validation-allowing': "csv",
            'data-validation-error-msg-mime': "You can only upload file in csv format."
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(args[1])
        store_id = args[1].get('store')
        Kitchen_id = store_id
        bool = False
        if args[1].get('kitchen'):
            Kitchen_id = args[1].get('kitchen')
            bool = True

        kitchen = self.get_kitchen(Kitchen_id, bool)

        stores = self.get_store(store_id)
        self.fields['store'].choices = stores
        self.fields['kitchen'].choices = kitchen

    def get_kitchen(self, id, bool):
        if bool:
            kitchens = Kitchen.objects.filter(id=id, is_deleted=False)
        else:
            kitchens = Kitchen.objects.filter(store_id=id, is_deleted=False)
        kitchen = (tuple((s.pk, s.name) for s in kitchens))
        return kitchen

    def get_store(self, id):
        stores = Store.objects.filter(id=id, is_deleted=False, status=True)
        store = (tuple((s.pk, s.name) for s in stores))
        return store
