from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/nobody.jpg')
    about_me = models.TextField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name='profiles')

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
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='events')
    participants = models.ManyToManyField(User, related_name='events')

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"

class NotificationSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_settings')
    new_message = models.BooleanField(default=True)
    new_event = models.BooleanField(default=True)
    new_skill = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification settings for {self.user.username}"