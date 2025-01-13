from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
import os
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill

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

@login_required
def profile(request):
    # Get the current user and their profile
    user = request.user
    profile = user.profile
    all_skills = Skill.objects.all()

    if request.method == 'POST':
        # Update profile picture if provided
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
        # Update Facebook link if provided
        if 'facebook_link' in request.POST:
            profile.facebook_link = request.POST['facebook_link']
            profile.save()
        # Update LinkedIn link if provided
        if 'linkedin_link' in request.POST:
            profile.linkedin_link = request.POST['linkedin_link']
            profile.save()
        # Update email if provided
        if 'email' in request.POST:
            user.email = request.POST['email']
            user.save()
        # Update about me section if provided
        if 'about_me' in request.POST:
            profile.about_me = request.POST['about_me']
            profile.save()
        # Update skills if provided
        if 'skills' in request.POST:
            profile.skills.set(request.POST.getlist('skills'))
            profile.save()
        # Redirect to the profile page after saving changes
        return redirect('profile')

    # Prepare context data for rendering the profile page
    context = {
        'user': user,
        'profile': profile,
        'all_skills': all_skills,
    }
    return render(request, 'main/profile.html', context)