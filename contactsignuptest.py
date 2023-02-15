from django.test import TestCase
from django.urls import reverse

from .models import Contact


class ContactFormTestCase(TestCase):
    def test_valid_form_submission(self):
        """
        Test that a valid form submission creates a new contact object and redirects to the success page.
        """
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '1234567890',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 302)  # should redirect to success page
        self.assertRedirects(response, reverse('contact_success'))
        self.assertEqual(Contact.objects.count(), 1)  # should create a new contact object
        contact = Contact.objects.first()
        self.assertEqual(contact.name, data['name'])
        self.assertEqual(contact.email, data['email'])
        self.assertEqual(contact.phone, data['phone'])
        self.assertEqual(contact.message, data['message'])

    def test_invalid_form_submission(self):
        """
        Test that an invalid form submission does not create a new contact object and shows the errors on the page.
        """
        data = {
            'name': '',
            'email': 'invalid_email',
            'phone': 'invalid_phone',
            'message': ''
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)  # should return the same page with errors
        self.assertContains(response, "This field is required.")
        self.assertContains(response, "Enter a valid email address.")
        self.assertContains(response, "Enter a valid phone number.")
        self.assertEqual(Contact.objects.count(), 0)  # should not create a new contact object