from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
import os
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data and send an email to the email host listed in the .env file
            EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

            # email content
            subject = 'Contact Form Submission'
            message = f"Name: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\nMessage: {form.cleaned_data['message']}"
            from_email = EMAIL_HOST_USER
            recipient_list = [EMAIL_HOST_USER]

            send_mail(subject, message, from_email, recipient_list)

            # Display a success message and redirect the user back to the contact page
            messages.success(request, 'Thank you for your message. We will get back to you shortly.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})

def terms_privacy(request):
    return render(request, 'main/terms_privacy.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

def skills(request):
    return render(request, 'main/skills.html')

def events(request):
    return render(request, 'main/events.html')

def messages_view(request):
    return render(request, 'main/messages.html')

def settings(request):
    return render(request, 'main/settings.html')

def profile(request):
    return render(request, 'main/profile.html')