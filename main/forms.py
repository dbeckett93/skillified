from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    reason = forms.ChoiceField(choices=[
        ('general', 'General Inquiry'),
        ('support', 'Support Request'),
        ('feedback', 'Feedback'),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send'))