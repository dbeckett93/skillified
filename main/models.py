from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
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

