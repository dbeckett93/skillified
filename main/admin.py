from django.contrib import admin
from .models import Profile, Skill, Event, NotificationSetting, Message

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Event)
admin.site.register(Message)
admin.site.register(NotificationSetting)