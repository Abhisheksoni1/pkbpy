from django import forms
from apps.stores.models import Category, Kitchen, Store


class ItemForm(forms.Form):
    OFFER_CHOICES = [
        (False, 'Disable'),
        (True, 'Enable')]

    FOOD_CHOICES = [(0, 'Vegetarian'), (1, 'Non-Vegetarian'),
                    (2, 'Eggetarian')]

    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required length',
            'data-validation-length': 'min2',
            'data-validation-error-msg-required': "You did not enter correct item name.",
            'data-validation-error-msg-length': "Please enter correct item name.",
            'placeholder': "Enter Item Name"
        })
    )

    short_description = forms.CharField(
        max_length=100,
        required=False,
        error_messages={'required': 'Please enter the short description.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'length',
            'data-validation-length': 'min2',
            'data-validation-error-msg': "You did not enter tag line.",
            'placeholder': "Short Description"

        })
    )

    description = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'data-validation': 'length',
            'data-validation-length': 'min2',
            'data-validation-error-msg': "You did not enter description line.",
            'placeholder': "Description"

        })
    )

    category_name = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "btn btn-primary btn-md",
            'data-parsley-multiple': 'gender'
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

    food_type = forms.ChoiceField(
        choices=FOOD_CHOICES,
        required=False,
        initial='Vegetarian',
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        }
        )
    )

    is_offer_active = forms.ChoiceField(
        choices=OFFER_CHOICES,
        required=False,
        initial=True,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        }
        )
    )

    is_outof_stock = forms.ChoiceField(
        choices=OFFER_CHOICES,
        required=False,
        initial=False,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        }
        )
    )

    base_price = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required number',
            'data-validation-length': 'max4',
            'data-validation-error-msg-required': "You did not enter the base price.",
            'data-validation-error-msg-float': "Please enter numeric values.",
            'placeholder': "Base Price"

        })
    )

    item_price_description = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            # 'data-validation': 'length',
            # 'data-validation-length': 'min2',
            # 'data-validation-error-msg': "You did not enter tag line.",
            'placeholder': "Item Price Description"

        })
    )

    kitchen = forms.ChoiceField(
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control kitchens",
            'data-parsley-multiple': 'gender'
        })
    )

    store = forms.ChoiceField(
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control stores",
            'data-parsley-multiple': 'gender'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        store = args[1]['store']
        kitchen = store
        bool = True
        if args[1].get('kitchen'):
            bool = False
            kitchen = args[1]['kitchen']

        categories = self.get_category(store)
        kitchen = self.get_kitchen(kitchen, bool)
        stores = self.get_store(store)
        self.fields['store'].choices = stores
        self.fields['kitchen'].choices = kitchen
        self.fields['category_name'].choices = categories
        # print(stores)

    def get_category(self, id):
        categories = Category.objects.filter(kitchen__store_id=id, is_deleted=False)
        category = (tuple((c.pk, c.name) for c in categories))
        return category

    def get_kitchen(self, id, bool):
        if bool:
            kitchens = Kitchen.objects.filter(store_id=id, is_deleted=False)
        if not bool:
            kitchens = Kitchen.objects.filter(id=id)
        kitchen = (tuple((s.pk, s.name) for s in kitchens))
        return kitchen

    def get_store(self, id):
        stores = Store.objects.filter(id=id, is_deleted=False)
        store = (tuple((s.pk, s.name) for s in stores))
        return store

    def clean_base_price(self):
        base_price = self.cleaned_data['base_price']
        if base_price:
            try:
                cod = float(base_price)
            except Exception:
                raise forms.ValidationError('Base price should be float value')
        return base_price

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if len(name) == 0:
    #         raise forms.ValidationError('name is required field')
    #     else:
    #         return name
    #


class UpdateItemForm(forms.Form):
    OFFER_CHOICES = [(True, 'Enable'),
                     (False, 'Disable')]

    FOOD_CHOICES = [(0, 'Vegetarian'), (1, 'Non-Vegetarian'),
                    (2, 'Eggetarian')]

    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required length',
            'data-validation-length': 'min2',
            'data-validation-error-msg-required': "You did not enter correct item name.",
            'data-validation-error-msg-length': "Please enter correct item name.",
            'placeholder': "Enter Item Name"
        })
    )

    short_description = forms.CharField(
        max_length=100,
        required=False,
        error_messages={'required': 'Please enter the short description.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'length',
            'data-validation-length': 'min2',
            'data-validation-error-msg': "You did not enter tag line.",
            'placeholder': "Short Description"

        })
    )

    description = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'data-validation': 'length',
            'data-validation-length': 'min2',
            'data-validation-error-msg': "You did not enter description line.",
            'placeholder': "Description"

        })
    )

    category_name = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "btn btn-primary btn-md",
            'data-parsley-multiple': 'gender'
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

    food_type = forms.ChoiceField(
        choices=FOOD_CHOICES,
        required=False,
        initial='Vegetarian',
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        }
        )
    )

    is_offer_active = forms.ChoiceField(
        choices=OFFER_CHOICES,
        required=False,
        initial=True,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        }
        )
    )

    is_outof_stock = forms.ChoiceField(
        choices=OFFER_CHOICES,
        required=False,
        initial=False,
        widget=forms.Select(attrs={
            'type': "radio",
            'class': "form-control",
            'data-parsley-multiple': 'gender'
        }
        )
    )

    base_price = forms.CharField(
        max_length=7,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required float',
            'data-validation-length': 'max7',
            'data-validation-error-msg-required': "You did not enter the base price.",
            'data-validation-error-msg-float': "Please enter numeric values.",
            'placeholder': "Base Price"

        })
    )

    item_price_description = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            # 'data-validation': 'length',
            # 'data-validation-length': 'min2',
            # 'data-validation-error-msg': "You did not enter tag line.",
            'placeholder': "Item Price Description"

        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_base_price(self):
        base_price = self.cleaned_data['base_price']
        if base_price:
            try:
                cod = float(base_price)
            except Exception:
                raise forms.ValidationError('Base price should be float value')
        return base_price