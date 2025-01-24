from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Event, Skill, Profile
from django.utils import timezone
from datetime import datetime


class EventDetailTests(TestCase):
    """
    Test suite for the Event Detail functionality.
    This test suite includes the following tests:
    - `test_event_detail_accessible_to_authenticated_users`: Ensures that 
      the event details page is accessible to authenticated users.

    - `test_event_detail_displays_correct_information`: Ensures that the 
      event details page displays the correct event information.

    - `test_register_for_event`: Ensures that users can register for an event.

    - `test_unregister_from_event`: Ensures that users can unregister from 
      an event.

    - `test_edit_delete_buttons_visible_to_owner`: Ensures that the "Edit 
      Event" and "Delete Event" buttons are only visible to the event owner.

    - `test_edit_event`: Ensures that the event owner can edit the event.
    
    - `test_delete_event`: Ensures that the event owner can delete the event.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='TestPassword1word1')
        self.other_user = User.objects.create_user(
            username='otheruser', password='TestPassword1word1')
        self.client.login(username='testuser', password='TestPassword1word1')

        self.skill = Skill.objects.create(
            name='Test Skill', description='Test Skill Description')
        self.event = Event.objects.create(
            title='Test Event',
            overview='Test Event Overview',
            date_time=timezone.make_aware(datetime(2025, 1, 21, 10, 0, 0)),
            skill=self.skill,
            owner=self.user
        )

    def test_event_detail_accessible_to_authenticated_users(self):
        response = self.client.get(
            reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_event_detail_displays_correct_information(self):
        response = self.client.get(
            reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')
        self.assertContains(response, 'Test Event Overview')
        self.assertContains(response, 'Jan. 21, 2025, 10 a.m.')

    def test_register_for_event(self):
        self.client.login(username='otheruser', password='TestPassword1word1')
        response = self.client.post(
            reverse('event_detail', args=[self.event.id]), {'action': 'register'})
        # Redirect after successful registration
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.event.participants.filter(
            id=self.other_user.id).exists())

    def test_unregister_from_event(self):
        self.client.login(username='otheruser', password='TestPassword1word1')
        self.event.participants.add(self.other_user)
        response = self.client.post(reverse('event_detail', args=[self.event.id]), {
                                    'action': 'unregister'})
        # Redirect after successful unregistration
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.event.participants.filter(
            id=self.other_user.id).exists())

    def test_edit_delete_buttons_visible_to_owner(self):
        response = self.client.get(
            reverse('event_detail', args=[self.event.id]))
        self.assertContains(response, 'Edit Event')
        self.assertContains(response, 'Delete Event')

        self.client.login(username='otheruser', password='TestPassword1word1')
        response = self.client.get(
            reverse('event_detail', args=[self.event.id]))
        self.assertNotContains(response, 'Edit Event')
        self.assertNotContains(response, 'Delete Event')

    def test_edit_event(self):
        response = self.client.post(reverse('edit_event', args=[self.event.id]), {
            'title': 'Updated Event Title',
            'overview': 'Updated Event Overview',
            'date_time': '2025-01-22 11:00:00'
        })
        # Redirect after successful form submission
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event Title')
        self.assertEqual(self.event.overview, 'Updated Event Overview')
        self.assertEqual(self.event.date_time, timezone.make_aware(
            datetime(2025, 1, 22, 11, 0, 0)))

    def test_delete_event(self):
        response = self.client.post(
            reverse('delete_event', args=[self.event.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        event_exists = Event.objects.filter(id=self.event.id).exists()
        self.assertFalse(event_exists)
