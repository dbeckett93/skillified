from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from main.models import NotificationSetting, Profile
import os

# Set the Django settings module environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'skillified.settings'


class SettingsViewTests(TestCase):
    """
    Unit tests for the SettingsView.

    This test case includes the following tests:
    - Test that the settings page renders correctly.
    - Test updating the username and email.
    - Test updating notification settings.
    - Test updating the password.
    - Test missing password confirmation.
    - Test incorrect current password.
    - Test new password too short.
    - Test new password without a digit.
    - Test new password without a letter.
    - Test new password without an uppercase letter.
    - Test new password without a lowercase letter.
    - Test new passwords do not match.

    Each test ensures that the settings view behaves as expected
    under various conditions.
    """
    @classmethod
    def setUpTestData(cls):
        # Create a test user and profile once for the entire test case
        cls.user = User.objects.create_user(
            username='testuser', password='TestPassword1')
        cls.profile, created = Profile.objects.get_or_create(user=cls.user)

    def setUp(self):
        # Create a client and log in the user for each test
        self.client = Client()
        self.client.login(username='testuser', password='TestPassword1')
        # Refresh the profile instance to avoid stale data
        self.profile = Profile.objects.get(user=self.user)

    # Test that the settings page renders correctly
    def test_settings_page_renders_correctly(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/settings.html')
        self.assertContains(response, 'User Settings')
        self.assertContains(response, 'Notification Settings')
        self.assertContains(response, 'Mentor Status')

    # Test updating the username and email
    def test_update_username_and_email(self):
        self.client.post(reverse('settings'), {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'current_password': '',
            'new_password': '',
            'confirm_password': '',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')

    # Test updating notification settings
    def test_update_notification_settings(self):
        self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': '',
            'new_password': '',
            'confirm_password': '',
            'notify_messages': 'on',
            'notify_events': '',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        notification_settings = NotificationSetting.objects.get(
            user=self.user)
        self.assertTrue(notification_settings.new_message)
        self.assertFalse(notification_settings.new_event)
        self.assertTrue(notification_settings.new_skill)

    # Test updating the password
    def test_update_password(self):
        self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123'))

    # Test missing password confirmation
    def test_password_confirmation_missing(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': 'NewPassword123',
            'confirm_password': '',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please confirm your new password.')

    # Test incorrect current password
    def test_current_password_incorrect(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'WrongPassword',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Current password is incorrect.')

    # Test new password too short
    def test_new_password_too_short(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': 'short',
            'confirm_password': 'short',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), (
                'New password must be at least 8 characters long.')
        )

    # Test new password without a digit
    def test_new_password_no_digit(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': 'NoDigitsHere',
            'confirm_password': 'NoDigitsHere',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'New password must contain at least one digit.')

    # Test new password without a letter
    def test_new_password_no_letter(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': '12345678',
            'confirm_password': '12345678',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'New password must contain at least one letter.')

    # Test new password without an uppercase letter
    def test_new_password_no_uppercase(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': 'lowercase1',
            'confirm_password': 'lowercase1',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), (
                'New password must contain at least one uppercase letter.')
        )

    # Test new password without a lowercase letter
    def test_new_password_no_lowercase(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': 'UPPERCASE1',
            'confirm_password': 'UPPERCASE1',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), (
                'New password must contain at least one lowercase letter.')
        )

    # Test new passwords do not match
    def test_new_passwords_do_not_match(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': 'NewPassword123',
            'confirm_password': 'DifferentPassword123',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
            'mentor_status': 'on',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'New passwords do not match.')
