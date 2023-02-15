from django.test import TestCase
from django.urls import reverse

class BookingViewTestCase(TestCase):
    def test_booking_view_status_code(self):
        # Ensure that the booking page returns a 200 status code.
        response = self.client.get(reverse('booking'))
        self.assertEqual(response.status_code, 200)

    def test_booking_view_template(self):
        # Ensure that the booking page uses the correct template.
        response = self.client.get(reverse('booking'))
        self.assertTemplateUsed(response, 'booking.html')

    def test_booking_view_post(self):
        # Ensure that submitting the booking form with valid data redirects to the correct page.
        response = self.client.post(reverse('booking'), {'search_location': '1', 'cin': '2023-02-14', 'cout': '2023-02-15', 'capacity': '2'})
        self.assertRedirects(response, reverse('book-room') + '?roomid=1')

    def test_booking_view_post_invalid_data(self):
        # Ensure that submitting the booking form with invalid data displays an error message.
        response = self.client.post(reverse('booking'), {'search_location': '1', 'cin': '2023-02-15', 'cout': '2023-02-14', 'capacity': '2'})
        self.assertContains(response, 'Check-in date should be before check-out date', status_code=200)

    def test_booking_view_no_rooms(self):
        # Ensure that the booking page displays a message when there are no available rooms.
        response = self.client.get(reverse('booking'))
        self.assertNotContains(response, 'Rooms Available')