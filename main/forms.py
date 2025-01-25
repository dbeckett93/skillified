from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from allauth.account.forms import SignupForm
from .models import Profile, Skill, Event


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    reason = forms.ChoiceField(
        choices=[
            ('general', 'General Inquiry'),
            ('support', 'Support Request'),
            ('feedback', 'Feedback'),
        ]
    )

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
        help_text=(
            'Mentors can list skills for other users to see and can arrange '
            'skill sharing events for the community.'
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.add_input(Submit('submit', 'Sign Up'))

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


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Skill'))


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'overview', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(
                attrs={'class': 'datetimepicker'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Event'))


class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'overview', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(
                attrs={'class': 'datetimepicker'}
            ),
        }
