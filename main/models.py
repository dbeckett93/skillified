from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Profile model represents the user's profile information.
# It is linked to the User model via a one-to-one relationship.
# This model includes fields for profile picture, about me section, social media links, skills, and mentor status.


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

# Skill model represents the skills that users can add to their profiles.
# It includes fields for the skill name, description, and timestamps for creation and updates.
# This model is related to the Profile model via a many-to-many relationship.


class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Event model represents the events that users can create and participate in.
# It includes fields for the event title, overview, date and time, and relationships to the Skill and User models.
# This model is related to the Skill model via a foreign key and to the User model via a many-to-many relationship for participants and a foreign key for the owner.


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

# NotificationSetting model represents the notification preferences for users.
# It includes fields for new message notifications, new event notifications, and new skill notifications.
# This model is related to the User model via a foreign key.


class NotificationSetting(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_settings')
    new_message = models.BooleanField(default=True)
    new_event = models.BooleanField(default=True)
    new_skill = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification settings for {self.user.username}"
