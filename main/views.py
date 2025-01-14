import json
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from .forms import ContactForm
from .models import Profile, Skill

# Home page view
def home(request):
    return render(request, 'main/home.html')

# About page view
def about(request):
    return render(request, 'main/about.html')

# Contact page view with form handling
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

# Terms and privacy page view
def terms_privacy(request):
    return render(request, 'main/terms_privacy.html')

# Dashboard page view
def dashboard(request):
    return render(request, 'main/dashboard.html')

# Skills page view
def skills(request):
    return render(request, 'main/skills.html')

# Events page view
def events(request):
    return render(request, 'main/events.html')

# Messages page view
def messages_view(request):
    return render(request, 'main/messages.html')

# Settings page view
def settings(request):
    return render(request, 'main/settings.html')

# Profile page view with profile update handling
@login_required
def profile(request):
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
            skill_ids = request.POST.getlist('skills')
            skills = Skill.objects.filter(id__in=skill_ids)
            profile.skills.set(skills)
            profile.save()
        # Add new skill if provided
        if 'new_skill' in request.POST:
            new_skill_name = request.POST['new_skill'].strip()
            if new_skill_name:
                new_skill, created = Skill.objects.get_or_create(name=new_skill_name)
                profile.skills.add(new_skill)
                profile.save()
        # Redirect to the profile page after saving changes
        return redirect('profile')

    context = {
        'user': user,
        'profile': profile,
        'all_skills': all_skills,
    }
    return render(request, 'main/profile.html', context)

# API endpoint to add a new skill
@login_required
@csrf_protect
def add_skill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        skill_name = data.get('name')
        if skill_name:
            new_skill, created = Skill.objects.get_or_create(name=skill_name)
            # Add the skill to the user's profile
            request.user.profile.skills.add(new_skill)
            return JsonResponse({'success': True, 'skill_id': new_skill.id, 'created': created})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid skill name'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# API endpoint to delete an existing skill
@login_required
@csrf_protect
def delete_skill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        skill_id = data.get('skill_id')
        if skill_id:
            try:
                skill = Skill.objects.get(id=skill_id)
                request.user.profile.skills.remove(skill)
                return JsonResponse({'success': True})
            except Skill.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Skill does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid skill ID'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# API endpoint to edit an existing skill
@login_required
@csrf_protect
def edit_skill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        skill_id = data.get('skill_id')
        skill_name = data.get('name')
        if skill_id and skill_name:
            try:
                skill = Skill.objects.get(id=skill_id)
                skill.name = skill_name
                skill.save()
                return JsonResponse({'success': True})
            except Skill.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Skill does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid skill ID or name'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})