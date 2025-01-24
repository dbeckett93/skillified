from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('image', blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name='profiles')
    is_mentor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    date_time = models.DateTimeField()
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='events')
    participants = models.ManyToManyField(User, related_name='events')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


class NotificationSetting(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_settings')
    new_message = models.BooleanField(default=True)
    new_event = models.BooleanField(default=True)
    new_skill = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification settings for {self.user.username}"
