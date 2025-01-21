from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Event, Skill
from django.utils import timezone
from datetime import datetime

class EventsTests(TestCase):
    """
    Test suite for the Events functionality.
    This test suite includes the following tests:
    - `test_search_events_by_keyword`: Tests the search functionality by querying events based on a keyword.
    - `test_search_events_by_date`: Tests the search functionality by querying events based on a date.
    - `test_search_events_empty_query`: Tests the search functionality with an empty query string.
    - `test_search_events_no_results`: Tests the search functionality with a query string that yields no results.
    Setup:
    - Creates a client for making HTTP requests.
    - Creates events for testing.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='TestPassword1word1')
        self.client.login(username='testuser', password='TestPassword1word1')

        self.skill = Skill.objects.create(name='Test Skill', description='Test Skill Description')
        self.event1 = Event.objects.create(
            title='Test Event 1',
            overview='Overview of Test Event 1',
            date_time=timezone.make_aware(datetime(2025, 1, 21, 10, 0, 0)),
            skill=self.skill,
            owner=self.user
        )
        self.event2 = Event.objects.create(
            title='Test Event 2',
            overview='Overview of Test Event 2',
            date_time=timezone.make_aware(datetime(2025, 1, 22, 11, 0, 0)),
            skill=self.skill,
            owner=self.user
        )

    def test_search_events_by_keyword(self):
        response = self.client.get(reverse('events') + '?q=Test Event 1')
        self.assertContains(response, 'Test Event 1')
        self.assertNotContains(response, 'Test Event 2')

    def test_search_events_by_date(self):
        response = self.client.get(reverse('events') + '?event_date=2025-01-21')
        self.assertContains(response, 'Test Event 1')
        self.assertNotContains(response, 'Test Event 2')

    def test_search_events_empty_query(self):
        response = self.client.get(reverse('events') + '?q=')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event 1')
        self.assertContains(response, 'Test Event 2')

    def test_search_events_no_results(self):
        response = self.client.get(reverse('events') + '?q=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Event 1')
        self.assertNotContains(response, 'Test Event 2')