import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillified.settings')
django.setup()

# Debug information
print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))
print("INSTALLED_APPS:", settings.INSTALLED_APPS)