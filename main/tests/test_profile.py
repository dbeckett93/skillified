from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Profile, Skill
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import json

class ProfilePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Debug information
        from django.conf import settings
        print("INSTALLED_APPS in test:", settings.INSTALLED_APPS)

        # Create a test user and profile once for the entire test case
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.profile, created = Profile.objects.get_or_create(user=cls.user)

    def setUp(self):
        # Create a client and log in the user for each test
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        # Refresh the profile instance to avoid stale data
        self.profile = Profile.objects.get(user=self.user)

    def test_add_profile_image(self):
        # Use an actual image file for the test
        with open('media/profile_pictures/nobody.jpg', 'rb') as img:
            self.profile.profile_picture = SimpleUploadedFile(name='nobody.jpg', content=img.read(), content_type='image/jpeg')
        self.profile.save()
        with open('media/profile_pictures/new_nobody.jpg', 'rb') as img:
            response = self.client.post(reverse('profile'), {'profile_picture': img})
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Print variables for debugging
        print("Response status code:", response.status_code)
        print("Profile picture URL:", self.profile.profile_picture.url)
        # Check that the profile picture was updated
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.profile_picture)

    def test_change_profile_image(self):
        # User with a profile image uses 'Change Picture' to add a new image
        with open('media/profile_pictures/nobody.jpg', 'rb') as img:
            self.profile.profile_picture = SimpleUploadedFile(name='nobody.jpg', content=img.read(), content_type='image/jpeg')
        self.profile.save()
        with open('media/profile_pictures/new_nobody.jpg', 'rb') as img:
            response = self.client.post(reverse('profile'), {'profile_picture': img})
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the profile picture was updated
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.profile_picture)

    def test_delete_profile_image(self):
        # User with a profile image clicks on 'Delete Picture'
        with open('media/profile_pictures/nobody.jpg', 'rb') as img:
            self.profile.profile_picture = SimpleUploadedFile(name='nobody.jpg', content=img.read(), content_type='image/jpeg')
        self.profile.save()
        # Simulate clicking the delete picture button
        response = self.client.post(reverse('delete_profile_picture'), json.dumps({'delete_profile_picture': 'true'}), content_type='application/json')
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Check that the profile picture was deleted
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.profile_picture, None)

    def test_profile_page_status_code(self):
        # Check that the profile page returns a 200 status code
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_template(self):
        # Check that the profile page uses the correct template
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'main/profile.html')

    def test_profile_page_context(self):
        # Check that the profile page context contains the correct user profile
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.context['user'].profile, self.profile)

    def test_profile_page_redirect_if_not_logged_in(self):
        # Check that the profile page redirects to login if the user is not logged in
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('profile')}")

    def test_update_contact_information(self):
        # User updates contact information
        response = self.client.post(reverse('profile'), {
            'facebook_link': 'https://facebook.com/testuser',
            'linkedin_link': 'https://linkedin.com/in/testuser',
            'email': 'testuser@example.com'
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the contact information was updated
        self.profile.refresh_from_db()
        self.user.refresh_from_db()  # Refresh the User instance
        self.assertEqual(self.profile.facebook_link, 'https://facebook.com/testuser')
        self.assertEqual(self.profile.linkedin_link, 'https://linkedin.com/in/testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_update_about_me(self):
        # User updates about me section
        response = self.client.post(reverse('profile'), {
            'about_me': 'This is a test about me section.'
        })
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the about me section was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.about_me, 'This is a test about me section.')

    def test_add_skill(self):
        # User adds a new skill
        response = self.client.post(reverse('add_skill'), {
            'name': 'Python',
            'description': 'Programming language'
        })
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the skill was added
        skill = Skill.objects.get(name='Python')
        self.assertEqual(skill.description, 'Programming language')
        self.assertIn(skill, self.profile.skills.all())

    def test_edit_skill(self):
        # User edits an existing skill
        skill = Skill.objects.create(name='Python')
        self.profile.skills.add(skill)
        response = self.client.post(reverse('edit_skill'), json.dumps({
            'skill_id': skill.id,
            'name': 'Advanced Python'
        }), content_type='application/json')
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Refresh the skill instance
        skill.refresh_from_db()
        # Check that the skill was updated
        self.assertEqual(skill.name, 'Advanced Python')

    def test_delete_skill(self):
        # User deletes an existing skill
        skill = Skill.objects.create(name='Python')
        self.profile.skills.add(skill)
        
        response = self.client.post(reverse('delete_skill'), json.dumps({
            'skill_id': skill.id
        }), content_type='application/json')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Refresh the profile instance
        self.profile.refresh_from_db()
        
        # Check that the skill was deleted from the database
        skill_exists = Skill.objects.filter(id=skill.id).exists()
        self.assertFalse(skill_exists)
        self.assertNotIn(skill, self.profile.skills.all())
