from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'skillified.settings'

class HomePageTests(TestCase):
    """
    Test suite for the Home Page of the application.

    This test suite includes the following tests:
    - Test the status code of the home page.
    - Test that the correct template is used for the home page.
    - Test that the home page contains the correct HTML content.
    - Test that the home page does not contain incorrect HTML content.
    - Test that the navigation links are present on the home page.
    - Test that authenticated users see the correct navigation links.

    Classes:
        HomePageTests: Contains tests for the home page.

    Methods:
        setUp: Sets up the test client and URLs for the tests.
        test_home_page_status_code: Tests that the home page returns a status code of 200.
        test_home_page_template: Tests that the correct template is used for the home page.
        test_home_page_contains_correct_html: Tests that the home page contains the correct HTML content.
        test_home_page_does_not_contain_incorrect_html: Tests that the home page does not contain incorrect HTML content.
        test_navigation_links: Tests that the navigation links are present on the home page.
        test_authenticated_user_navigation_links: Tests that authenticated users see the correct navigation links.
    """
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.about_url = reverse('about')
        self.contact_url = reverse('contact')
        self.terms_privacy_url = reverse('terms_privacy')
        self.login_url = reverse('account_login')

    def test_home_page_status_code(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, '<h1>Learn, Share, Thrive</h1>')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get(self.home_url)
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

    def test_navigation_links(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, f'href="{self.home_url}"')
        self.assertContains(response, f'href="{self.about_url}"')
        self.assertContains(response, f'href="{self.contact_url}"')
        self.assertContains(response, f'href="{self.terms_privacy_url}"')
        self.assertContains(response, f'href="{self.login_url}"')

    def test_authenticated_user_navigation_links(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.home_url)
        self.assertContains(response, f'href="{reverse("profile")}"')
        self.assertContains(response, f'href="{reverse("dashboard")}"')
        self.assertContains(response, f'href="{reverse("mentor_skills")}"')
        self.assertContains(response, f'href="{reverse("events")}"')
        self.assertContains(response, f'href="{reverse("settings")}"')
        self.assertContains(response, 'Logout')