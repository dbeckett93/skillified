from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from main.forms import ContactForm


class ContactPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')

    def test_contact_page_renders_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact.html')
        self.assertContains(response, 'Contact Us')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_form_submission_success(self):
        form_data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'message': 'This is a test message.'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_contact_form_submission_missing_fields(self):
        form_data = {
            'name': '',
            'email': 'testuser@example.com',
            'message': ''
        }
        response = self.client.post(self.url, data=form_data)
        # Form re-rendered with errors
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertIn('message', form.errors)
        self.assertEqual(form.errors['message'], ['This field is required.'])

    def test_contact_form_invalid_email(self):
        form_data = {
            'name': 'Test User',
            'email': 'invalid-email',
            'message': 'This is a test message.'
        }
        response = self.client.post(self.url, data=form_data)
        # Form re-rendered with errors
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], [
                         'Enter a valid email address.'])
