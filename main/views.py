from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def terms_privacy(request):
    return render(request, 'main/terms_privacy.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

def skills(request):
    return render(request, 'main/skills.html')

def events(request):
    return render(request, 'main/events.html')

def messages(request):
    return render(request, 'main/messages.html')

def settings(request):
    return render(request, 'main/settings.html')

def profile(request):
    return render(request, 'main/profile.html')