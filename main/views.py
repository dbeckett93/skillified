import json
import os

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q

from .forms import ContactForm, SkillForm
from .models import Profile, Skill, Event, NotificationSetting, Message

# Home page view
def home(request):
    """
    Renders the home page.
    """
    return render(request, 'main/home.html')

# About page view
def about(request):
    """
    Renders the about page.
    """
    return render(request, 'main/about.html')

# Contact page view with form handling
def contact(request):
    """
    Handles the contact form submission. If the form is valid, sends an email
    to the site admin and displays a success message.
    """
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
    """
    Renders the terms and privacy page.
    """
    return render(request, 'main/terms_privacy.html')

# Dashboard page view
def dashboard(request):
    """
    Renders the user dashboard page.
    """
    return render(request, 'main/dashboard.html')

# Logout page view
def logout(request):
    """
    Renders the logout confirmation page.
    """
    return render(request, 'account/logout.html')

# Events page view
def events(request):
    """
    Renders the events page.
    """
    return render(request, 'main/events.html')

# Messages page view
def messages_view(request):
    """
    Renders the messages page.
    """
    return render(request, 'main/messages.html')

# Settings page view
@login_required
def settings(request):
    """
    Handles the settings form submission. Allows the user to update their
    username, email, password, and notification settings.
    """
    if request.method == 'POST':
        user = request.user
        profile = user.profile

        username = request.POST.get('username')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        notify_messages = request.POST.get('notify_messages') == 'on'
        notify_events = request.POST.get('notify_events') == 'on'
        notify_skills = request.POST.get('notify_skills') == 'on'

        if username:
            user.username = username
        if email:
            user.email = email
        if current_password and new_password and not confirm_password:
            messages.error(request, 'Please confirm your new password.')
            return redirect('settings')
        elif current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if len(new_password) < 8:
                    messages.error(request, 'New password must be at least 8 characters long.')
                    return redirect('settings')
                if not any(char.isdigit() for char in new_password):
                    messages.error(request, 'New password must contain at least one digit.')
                    return redirect('settings')
                if not any(char.isalpha() for char in new_password):
                    messages.error(request, 'New password must contain at least one letter.')
                    return redirect('settings')
                if not any(char.isupper() for char in new_password):
                    messages.error(request, 'New password must contain at least one uppercase letter.')
                    return redirect('settings')
                if not any(char.islower() for char in new_password):
                    messages.error(request, 'New password must contain at least one lowercase letter.')
                    return redirect('settings')
                if new_password == confirm_password:
                    user.set_password(new_password)
                    update_session_auth_hash(request, user)
                else:
                    messages.error(request, 'New passwords do not match.')
                    return redirect('settings')
            else:
                messages.error(request, 'Current password is incorrect.')
                return redirect('settings')

        # Update notification settings
        notification_settings, created = NotificationSetting.objects.get_or_create(user=user)
        notification_settings.new_message = notify_messages
        notification_settings.new_event = notify_events
        notification_settings.new_skill = notify_skills
        notification_settings.save()

        user.save()
        profile.save()

        messages.success(request, 'Settings updated successfully.')
        return redirect('settings')

    return render(request, 'main/settings.html')

# Profile page view with profile update handling
@login_required
def profile(request):
    """
    Handles the profile update form submission. Allows the user to update their
    profile picture, social links, email, about me section, and skills.
    """
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
    """
    Adds a new skill to the user's profile if the request method is POST and
    the required data is provided.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            skill, created = Skill.objects.get_or_create(name=name, description=description)
            request.user.profile.skills.add(skill)
            return redirect('profile')
    return JsonResponse({'error': 'Invalid data'}, status=400)

# API endpoint to delete an existing skill
@login_required
@csrf_protect
def delete_skill(request):
    """
    Deletes an existing skill from the user's profile if the request method is
    POST and the skill ID is provided.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        skill_id = data.get('skill_id')
        if skill_id:
            try:
                skill = Skill.objects.get(id=skill_id)
                request.user.profile.skills.remove(skill)
                skill.delete()  # Delete the skill from the database
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
    """
    Edits an existing skill in the user's profile if the request method is POST
    and the required data is provided.
    """
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

# API endpoint to delete the user's profile picture
@login_required
@csrf_protect
def delete_profile_picture(request):
    """
    Deletes the user's profile picture if the request method is POST and the
    'delete_profile_picture' key is present in the request body.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('delete_profile_picture'):
            profile = request.user.profile
            profile.profile_picture = ''
            profile.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Mentor Skills page view
@login_required
def mentor_skills(request):
    """
    Renders the mentor skills page, displaying all skills added by any mentor.
    If the user is a mentor, they can add new skills. Supports keyword search.
    """
    query = request.GET.get('q')
    if query:
        skills = Skill.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            profiles__user__profile__is_mentor=True
        ).distinct()
    else:
        skills = Skill.objects.filter(profiles__user__profile__is_mentor=True).distinct()
    
    is_mentor = request.user.profile.is_mentor
    return render(request, 'main/mentor_skills.html', {'skills': skills, 'is_mentor': is_mentor, 'query': query})

# View to add a new skill for mentors
@login_required
def mentor_add_skill(request):
    """
    Allows mentors to add new skills. If the user is not a mentor, they are
    redirected to the mentor skills page. Handles both GET and POST requests.
    """
    if not request.user.profile.is_mentor:
        return redirect('mentor_skills')
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            request.user.profile.skills.add(skill)
            return redirect('mentor_skills')
    else:
        form = SkillForm()
    
    return render(request, 'main/mentor_add_skill.html', {'form': form})

# Skill detail page view
def skill_detail(request, skill_id):
    """
    Renders the skill detail page, displaying the details of a specific skill
    identified by the skill_id parameter.
    """
    skill = get_object_or_404(Skill, id=skill_id)
    return render(request, 'main/skill_detail.html', {'skill': skill})