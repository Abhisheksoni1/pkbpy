from django import forms


class FaqsForm(forms.Form):
    CHOICES = [('0', 'Enable'),
               ('1', 'Disable')]

    question = forms.CharField(
        max_length=80,
        required=False,
        error_messages={'required': 'Please enter the question.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required length',
            'data-validation-length': 'min2',
            'data-validation-error-msg-required': "You did not enter question.",
            'data-validation-error-msg-length': "Please Enter question more than 2 characters.",
            'placeholder': 'Enter question'
        })
    )

    short_answer = forms.CharField(
        max_length=80,
        required=False,
        error_messages={'required': 'Please enter the short answer.'},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'data-validation': 'required length',
            'data-validation-length': 'min4',
            'data-validation-error-msg-required': "You did not enter short answer.",
            'data-validation-error-msg-length': "Please enter short answer more than 4 characters.",
            'placeholder': "Short answer"

        })
    )

    answer = forms.CharField(
        max_length=1000,
        required=False,
        error_messages={'required': 'Please enter the answer.'},
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'data-validation': 'required length',
            'data-validation-length': 'min10',
            'data-validation-error-msg-required': "You did not enter the answer.",
            'data-validation-error-msg-length': "Please enter answer more than 10 characters.",
            'placeholder': "Answer"
        }
        )
    )

    def clean_question(self):
        data = self.cleaned_data['question']
        if len(data)< 2:
            raise forms.ValidationError("Please Enter more than 2 characters")
        return data

    def clean_short_answer(self):
        data = self.cleaned_data['short_answer']
        if len(data) < 4:
            raise forms.ValidationError("Please Enter more than 4 characters")
        return data

    def clean_answer(self):
        data = self.cleaned_data['answer']
        if (len(data) - data.count(' ')) < 10:
            raise forms.ValidationError("Please enter more than 10 characters")
        return data

