from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Profile, Skill
from django.core.files.uploadedfile import SimpleUploadedFile
import os

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
            image = SimpleUploadedFile(name='nobody.jpg', content=img.read(), content_type='image/jpeg')
            response = self.client.post(reverse('profile'), {'profile_picture': image})
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
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
        response = self.client.post(reverse('delete_profile_picture'), {'delete_profile_picture': True})
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Check that the profile picture was deleted
        self.profile.refresh_from_db()
        self.assertIn(self.profile.profile_picture, [None, 'https://i.imgur.com/2Q3XOlp.jpeg'])

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

    def test_profile_picture_upload_invalid_file(self):
        # User tries to upload an invalid file as profile picture
        invalid_file = SimpleUploadedFile(name='invalid_file.txt', content=b"fake text data", content_type='text/plain')
        response = self.client.post(reverse('profile'), {'profile_picture': invalid_file})
        # Check that the response status code is 200 (form error)
        self.assertEqual(response.status_code, 200)
        # Check that the profile picture was not updated
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.profile_picture)

    def test_profile_picture_upload_large_file(self):
        # User tries to upload a large file as profile picture
        large_file = SimpleUploadedFile(name='large_image.jpg', content=b'a' * (10 * 1024 * 1024), content_type='image/jpeg')
        response = self.client.post(reverse('profile'), {'profile_picture': large_file})
        # Check that the response status code is 200 (form error)
        self.assertEqual(response.status_code, 200)
        # Check that the profile picture was not updated
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.profile_picture)

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
        skill = Skill.objects.create(name='Python', description='Programming language')
        self.profile.skills.add(skill)
        response = self.client.post(reverse('edit_skill'), {
            'skill_id': skill.id,
            'name': 'Advanced Python',
            'description': 'Advanced programming language'
        })
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the skill was updated
        skill.refresh_from_db()
        self.assertEqual(skill.name, 'Advanced Python')
        self.assertEqual(skill.description, 'Advanced programming language')

    def test_delete_skill(self):
        # User deletes an existing skill
        skill = Skill.objects.create(name='Python', description='Programming language')
        self.profile.skills.add(skill)
        response = self.client.post(reverse('delete_skill'), {
            'skill_id': skill.id
        })
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the skill was deleted
        self.assertFalse(Skill.objects.filter(id=skill.id).exists())
        self.assertNotIn(skill, self.profile.skills.all())