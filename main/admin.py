from django.contrib import admin
from .models import Profile, Skill, Event, NotificationSetting

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Event)
admin.site.register(NotificationSetting)
