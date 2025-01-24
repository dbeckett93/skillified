from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Event, Skill, Profile
from django.utils import timezone
from datetime import datetime


class AddEventTests(TestCase):
    """
    Test suite for the Add Event functionality.
    This test suite includes the following tests:
    - `test_page_visible_to_mentor`: Ensures that the add event page is only
      visible to mentor users.

    - `test_page_not_visible_to_non_mentor`: Ensures that the add event page
      is not visible to non-mentor users.

    - `test_add_event`: Ensures that a mentor user can add a new event with a
      title, overview, and date/time.

    - `test_add_event_title_required`: Ensures that the event title is a
      required field.

    - `test_add_event_overview_required`: Ensures that the event overview is a
      required field.

    - `test_add_event_date_time_required`: Ensures that the event date/time is
      a required field.
      
    - `test_add_event_invalid_date_time_format`: Ensures that the event
      date/time format is validated.
    """

    def setUp(self):
        self.client = Client()
        self.mentor_user = User.objects.create_user(
            username='mentoruser', password='TestPassword1word1')
        self.non_mentor_user = User.objects.create_user(
            username='nonmentoruser', password='TestPassword1word1')

        self.mentor_profile, created = Profile.objects.get_or_create(
            user=self.mentor_user)
        self.mentor_profile.is_mentor = True
        self.mentor_profile.save()

        self.non_mentor_profile, created = Profile.objects.get_or_create(
            user=self.non_mentor_user)
        self.non_mentor_profile.is_mentor = False
        self.non_mentor_profile.save()

        self.skill = Skill.objects.create(
            name='Test Skill', description='Test Skill Description')

    def test_page_visible_to_mentor(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('add_event', args=[self.skill.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Event for Test Skill')

    def test_page_not_visible_to_non_mentor(self):
        self.client.login(username='nonmentoruser',
                          password='TestPassword1word1')
        response = self.client.get(reverse('add_event', args=[self.skill.id]))
        # Redirect to skill detail page
        self.assertEqual(response.status_code, 302)

    def test_add_event(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.post(reverse('add_event', args=[self.skill.id]), {
            'title': 'Test Event',
            'overview': 'Test Event Overview',
            'date_time': '2025-01-21 10:00'
        })
        # Redirect after successful form submission
        self.assertEqual(response.status_code, 302)
        event_exists = Event.objects.filter(
            title='Test Event', overview='Test Event Overview').exists()
        self.assertTrue(event_exists)

    def test_add_event_title_required(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.post(reverse('add_event', args=[self.skill.id]), {
            'title': '',
            'overview': 'Test Event Overview',
            'date_time': '2025-01-21 10:00'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])

    def test_add_event_overview_required(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.post(reverse('add_event', args=[self.skill.id]), {
            'title': 'Test Event',
            'overview': '',
            'date_time': '2025-01-21 10:00'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('overview', form.errors)
        self.assertEqual(form.errors['overview'], ['This field is required.'])

    def test_add_event_date_time_required(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.post(reverse('add_event', args=[self.skill.id]), {
            'title': 'Test Event',
            'overview': 'Test Event Overview',
            'date_time': ''
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('date_time', form.errors)
        self.assertEqual(form.errors['date_time'], ['This field is required.'])

    def test_add_event_invalid_date_time_format(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.post(reverse('add_event', args=[self.skill.id]), {
            'title': 'Test Event',
            'overview': 'Test Event Overview',
            'date_time': 'invalid-date-time'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('date_time', form.errors)
        self.assertEqual(form.errors['date_time'], [
                         'Enter a valid date/time.'])
