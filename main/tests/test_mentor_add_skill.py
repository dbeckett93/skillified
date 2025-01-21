from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Skill, Profile

class MentorAddSkillTests(TestCase):
    """
    Test suite for the Mentor Add Skill functionality.
    This test suite includes the following tests:
    - `test_page_visible_to_mentor`: Ensures that the add skill page is only visible to mentor users.
    - `test_page_not_visible_to_non_mentor`: Ensures that the add skill page is not visible to non-mentor users.
    - `test_add_skill`: Ensures that a mentor user can add a new skill with a name and description.
    - `test_add_skill_name_required`: Ensures that the skill name is a required field.
    - `test_add_skill_description_required`: Ensures that the skill description is a required field.
    - `test_add_skill_name_max_length`: Ensures that the skill name does not exceed 255 characters.
    """

    def setUp(self):
        self.client = Client()
        self.mentor_user = User.objects.create_user(username='mentoruser', password='TestPassword1word1')
        self.non_mentor_user = User.objects.create_user(username='nonmentoruser', password='TestPassword1word1')
        
        self.mentor_profile, created = Profile.objects.get_or_create(user=self.mentor_user)
        self.mentor_profile.is_mentor = True
        self.mentor_profile.save()
        
        self.non_mentor_profile, created = Profile.objects.get_or_create(user=self.non_mentor_user)
        self.non_mentor_profile.is_mentor = False
        self.non_mentor_profile.save()

    def test_page_visible_to_mentor(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('mentor_add_skill'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Skill')

    def test_page_not_visible_to_non_mentor(self):
        self.client.login(username='nonmentoruser', password='TestPassword1word1')
        response = self.client.get(reverse('mentor_add_skill'))
        self.assertEqual(response.status_code, 302)  # Redirect to mentor skills page

    def test_add_skill(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.post(reverse('mentor_add_skill'), {
            'name': 'Test Skill',
            'description': 'Test Skill Description'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        skill_exists = Skill.objects.filter(name='Test Skill', description='Test Skill Description').exists()
        self.assertTrue(skill_exists)

    def test_add_skill_name_required(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.post(reverse('mentor_add_skill'), {
            'name': '',
            'description': 'Test Skill Description'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['This field is required.'])

    def test_add_skill_description_required(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        response = self.client.post(reverse('mentor_add_skill'), {
            'name': 'Test Skill',
            'description': ''
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('description', form.errors)
        self.assertEqual(form.errors['description'], ['This field is required.'])

    def test_add_skill_name_max_length(self):
        self.client.login(username='mentoruser', password='TestPassword1word1')
        long_name = 'a' * 256
        response = self.client.post(reverse('mentor_add_skill'), {
            'name': long_name,
            'description': 'Test Skill Description'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['Ensure this value has at most 255 characters (it has 256).'])