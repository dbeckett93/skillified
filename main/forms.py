from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from allauth.account.forms import SignupForm
from .models import Profile

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

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    mentor = forms.ChoiceField(
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
        ],
        widget=forms.RadioSelect,
        label='Do you want to be a mentor and share skills with others?',
        help_text='Mentors can list skills for other users to see and can arrange skill sharing events for the community.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mentor'].help_text = 'Mentors can list skills for other users to see and can arrange skill sharing events for the community.'
        self.fields['mentor'].help_text = '<br>' + self.fields['mentor'].help_text

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
        # Update the profile with the mentor status
        profile = Profile.objects.get(user=user)
        profile.is_mentor = self.cleaned_data['mentor'] == 'yes'
        profile.save()
        
        return user