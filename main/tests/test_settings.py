from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from main.models import NotificationSetting, Profile
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'skillified.settings'

class SettingsViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user and profile once for the entire test case
        cls.user = User.objects.create_user(username='testuser', password='TestPassword1')
        cls.profile, created = Profile.objects.get_or_create(user=cls.user)

    def setUp(self):
        # Create a client and log in the user for each test
        self.client = Client()
        self.client.login(username='testuser', password='TestPassword1')
        # Refresh the profile instance to avoid stale data
        self.profile = Profile.objects.get(user=self.user)

    def test_settings_page_renders_correctly(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/settings.html')
        self.assertContains(response, 'User Settings')
        self.assertContains(response, 'Notification Settings')

    def test_update_username_and_email(self):
        response = self.client.post(reverse('settings'), {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'current_password': '',
            'new_password': '',
            'confirm_password': '',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_update_notification_settings(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': '',
            'new_password': '',
            'confirm_password': '',
            'notify_messages': 'on',
            'notify_events': '',
            'notify_skills': 'on',
        })
        notification_settings = NotificationSetting.objects.get(user=self.user)
        self.assertTrue(notification_settings.new_message)
        self.assertFalse(notification_settings.new_event)
        self.assertTrue(notification_settings.new_skill)

    def test_update_password(self):
        response = self.client.post(reverse('settings'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'current_password': 'TestPassword1',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
            'notify_messages': 'on',
            'notify_events': 'on',
            'notify_skills': 'on',
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123'))

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
            })
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), 'Please confirm your new password.')

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
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Current password is incorrect.')

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
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'New password must be at least 8 characters long.')

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
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'New password must contain at least one digit.')

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
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'New password must contain at least one letter.')

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
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'New password must contain at least one uppercase letter.')

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
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'New password must contain at least one lowercase letter.')

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
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'New passwords do not match.')