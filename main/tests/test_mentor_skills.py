from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Skill, Profile
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'skillified.settings'


class MentorSkillsTests(TestCase):
    """
    Test suite for the Mentor Skills functionality.
    This test suite includes the following tests:
    - `test_add_new_skill_button_not_visible_for_non_mentors`: Ensures
      that the "Add New Skill" button is not visible to users who are
      not mentors.

    - `test_add_new_skill_button_visible_for_mentors`: Ensures that the
      "Add New Skill" button is visible to users who are mentors.

    - `test_search_skills_by_description`: Tests the search
      functionality by querying skills based on their description.

    - `test_search_skills_by_title`: Tests the search functionality by
      querying skills based on their title.

    - `test_search_skills_empty_query`: Tests the search functionality
      with an empty query string.

    - `test_search_skills_no_results`: Tests the search functionality
      with a query string that yields no results.

    Setup:
    - Creates a client for making HTTP requests.
    - Creates a mentor user and a non-mentor user.
    - Sets up profiles for both users, marking one as a mentor and the
      other as a non-mentor.
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

    def test_add_new_skill_button_not_visible_for_non_mentors(self):
        self.client.login(
            username='nonmentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('mentor_skills'))
        self.assertNotContains(response, 'Add New Skill')

    def test_add_new_skill_button_visible_for_mentors(self):
        self.client.login(
            username='mentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('mentor_skills'))
        self.assertContains(response, 'Add New Skill')

    def test_search_skills_by_description(self):
        self.client.login(
            username='mentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('mentor_skills') + '?q=description')
        self.assertEqual(response.status_code, 200)

    def test_search_skills_by_title(self):
        self.client.login(
            username='mentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('mentor_skills') + '?q=title')
        self.assertEqual(response.status_code, 200)

    def test_search_skills_empty_query(self):
        self.client.login(
            username='mentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('mentor_skills') + '?q=')
        self.assertEqual(response.status_code, 200)

    def test_search_skills_no_results(self):
        self.client.login(
            username='mentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('mentor_skills') + '?q=nonexistent')
        self.assertEqual(response.status_code, 200)
