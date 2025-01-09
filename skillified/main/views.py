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