from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Skill, Profile, Event
from django.utils import timezone
from datetime import datetime


class SkillDetailTests(TestCase):
    """
    Test suite for the Skill Detail functionality.
    This test suite includes the following tests:
    - `test_edit_skill`: Ensures that a skill can be edited.
    - `test_delete_skill`: Ensures that a skill can be deleted.
    - `test_view_event_redirect`: Ensures that the "View Event" button 
      for an added event redirects to the correct page.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='TestPassword1word1')
        self.client.login(username='testuser', password='TestPassword1word1')

        self.skill = Skill.objects.create(
            name='Test Skill', description='Test Skill Description')
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.profile.skills.add(self.skill)

        self.event = Event.objects.create(
            title='Test Event',
            overview='Test Event Overview',
            date_time=timezone.make_aware(datetime(2025, 1, 21, 10, 0, 0)),
            skill=self.skill,
            owner=self.user
        )

    def test_edit_skill(self):
        response = self.client.post(reverse('edit_skill_detail'), {
            'skill_id': self.skill.id,
            'name': 'Updated Skill Name',
            'description': 'Updated Skill Description'
        })
        self.assertEqual(response.status_code, 302)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, 'Updated Skill Name')
        self.assertEqual(self.skill.description, 'Updated Skill Description')

    def test_delete_skill(self):
        response = self.client.post(
            reverse('delete_skill', args=[self.skill.id]), follow=True)
        skill_exists = Skill.objects.filter(id=self.skill.id).exists()
        self.assertFalse(skill_exists)

    def test_view_event_redirect(self):
        response = self.client.get(
            reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')
