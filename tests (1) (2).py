# Import necessary modules
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Contact, Review

# Define the test class
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.homepage_url = reverse('homepage')
        self.aboutpage_url = reverse('aboutpage')
        self.contactpage_url = reverse('contactpage')
        self.user_sign_up_url = reverse('user_sign_up')
        self.staff_sign_up_url = reverse('staff_sign_up')
        self.user_log_sign_page_url = reverse('user_log_sign_page')
        self.logoutuser_url = reverse('logoutuser')
        self.reviewsPage_url = reverse('reviewsPage')
        self.handleContact_url = reverse('handleContact')

    # Define tests for homepage view
    def test_homepage_GET(self):
        response = self.client.get(self.homepage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_homepage_POST(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.homepage_url, {
            'search_location': 1,
            'capacity': 2,
            'cin': '2022-04-01',
            'cout': '2022-04-05'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # Define tests for aboutpage view
    def test_aboutpage_GET(self):
        response = self.client.get(self.aboutpage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    # Define tests for contactpage view
    def test_contactpage_GET(self):
        response = self.client.get(self.contactpage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    # Define tests for handleContact view
    def test_handleContact_POST(self):
        response = self.client.post(self.handleContact_url, {
            'name': 'testuser',
            'email': 'testemail@test.com',
            'phone': '1234567890',
            'message': 'test message'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, 'http://127.0.0.1:8000/')

    # Define tests for reviewsPage view
    def test_reviewsPage_GET(self):
        response = self.client.get(self.reviewsPage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews.html')

    def test_reviewsPage_POST(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.reviewsPage_url, {
            'title': 'test review',
            'text': 'test review text',
            'rating': 3,
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.reviewsPage_url)

    # Define tests for user_sign_up view
    def test_user_sign_up_POST(self):
        response = self.client.post(self.user_sign_up_url, {
            'username': 'testuser',
            'password1': 'testpass',
            'password2': 'testpass'
        })
        self.assertEquals(response.status_code, 302)
    from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Contact, Hotels, Reservation


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.staff = User.objects.create_user(
            username='staffuser', password='staffpass', is_staff=True
        )
        self.hotel = Hotels.objects.create(
            owner='Test Owner', location='Test City', state='Test State', country='Test Country'
        )
        self.reservation = Reservation.objects.create(
            guest=self.user, hotel=self.hotel, check_in='2023-04-01', check_out='2023-04-05', 
            num_guests=2, total_price=500
        )

    def test_user_bookings_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/mybookings.html')
        self.assertContains(response, 'Test City')
        self.assertContains(response, 'No Bookings Found', count=0)

    def test_user_bookings_view_with_unauthenticated_user(self):
        response = self.client.get(reverse('user_bookings'))
        self.assertRedirects(response, '/user/login/?next=/user/bookings/')

    def test_add_new_location_view_with_staff_user_and_unique_location(self):
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.post(reverse('add_new_location'), 
            {'new_owner': 'New Owner', 'new_city': 'New City', 'new_state': 'New State', 'new_country': 'New Country'})
        self.assertRedirects(response, '/staff/')
        self.assertTrue(Hotels.objects.filter(location='New City', state='New State').exists())
        self.assertContains(response, 'New Location Has been Added Successfully')
        self.assertContains(response, 'Sorry City at this Location already exist', count=0)

    def test_add_new_location_view_with_staff_user_and_existing_location(self):
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.post(reverse('add_new_location'), 
            {'new_owner': 'New Owner', 'new_city': 'Test City', 'new_state': 'Test State', 'new_country': 'Test Country'})
        self.assertRedirects(response, '/staff/')
        self.assertFalse(Hotels.objects.filter(location='Test City', state='Test State').count() > 1)
        self.assertContains(response, 'Sorry City at this Location already exist')
        self.assertContains(response, 'New Location Has been Added Successfully', count=0)

    def test_add_new_location_view_with_unauthenticated_user(self):
        response = self.client.get(reverse('add_new_location'))
        self.assertRedirects(response, '/staff/login/?next=/staff/add_location/')
        response = self.client.post(reverse('add_new_location'), 
            {'new_owner': 'New Owner', 'new_city': 'New City', 'new_state': 'New State', 'new_country': 'New Country'})
        self.assertRedirects(response, '/staff/login/?next=/staff/add_location/')
        self.assertFalse(Hotels.objects.filter(location='New City', state='New State').exists())

   

