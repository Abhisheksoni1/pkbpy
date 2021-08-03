from django import forms
from apps.common.models import Page
import magic

STATUS_CHOICE = (('0', "Inactive"), ('1', "Active"))


class PageForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=100,
        error_messages={'required': 'Please enter title.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12',
                   'label': 'title',
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
                                             'data-validation': 'required',
                                             'data - validation - error - msg': 'Description is required field',

                                             }

                                  ))

    keywords = forms.CharField(max_length=600,
                               error_messages={'required': 'Please enter keywords.'},
                               required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'data-validation': 'required',
                                          'data - validation - error - msg': 'Keywords is required field',

                                          }
                               ))

    content = forms.CharField(
        error_messages={'required': 'Content is required field.'},
        widget=forms.Textarea(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'data-validation': 'required',
            'data-validation-error-msg': 'Content is required field'
        }
        )
    )

    status = forms.ChoiceField(
        initial='1',
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
            'data-validation-error-msg-mime': 'You can only upload images.'
        }))


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

    def clean_content(self):
        data = self.cleaned_data['content']
        if data is None:
            raise forms.ValidationError('Content is required field')
        return data

    def clean_keywords(self):

        data = self.cleaned_data['keywords']
        if data is None:
            raise forms.ValidationError('keywords is required filed')
        return data


