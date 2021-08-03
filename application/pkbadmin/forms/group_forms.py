from django import forms


class GroupForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=False,
        error_messages={'required': 'Please enter the role name.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required length',
            'data-validation-length': '2-50',
            'data-validation-error-msg-length': "You did not enter correct group name.",
            'data-validation-error-msg-required': "You did not enter group name.",
            'placeholder': "Enter Name"
        })
    )

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) < 2 and len(data) > 50:
            raise forms.ValidationError("Please enter valid group name.")
        return data
