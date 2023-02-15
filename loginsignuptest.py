from django.test import TestCase
from django.urls import reverse

class LoginSignupTests(TestCase):

    def test_login_form(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_signup_form(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Signup')

    def test_login_submit(self):
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'pswd': 'testpassword',
            'remember': True
        })
        self.assertEqual(response.status_code, 200)
        # Add additional assertions as needed

    def test_signup_submit(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        # Add additional assertions as needed

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'email': 'invaliduser@example.com',
            'pswd': 'invalidpassword',
            'remember': False
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')

    def test_signup_with_mismatched_passwords(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'mismatchedpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords must match')