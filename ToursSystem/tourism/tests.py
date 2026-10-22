from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tourism.models import Destination, TourPackage, Booking, Payment, Review, ContactMessage


class TourismSystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Admin user
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='adminpassword123'
        )

        # Regular customer
        self.customer = User.objects.create_user(
            username='customer_test',
            email='customer@test.com',
            password='customerpassword123',
            first_name='Alex',
            last_name='Traveler'
        )

        # Sample Destination
        self.destination = Destination.objects.create(
            name='Bali Island',
            country='Indonesia',
            city='Denpasar',
            description='Tropical island with beaches and culture.',
            best_time_to_visit='May - September',
            climate='Tropical',
            is_featured=True
        )

        # Sample Package
        self.package = TourPackage.objects.create(
            destination=self.destination,
            title='Bali 5-Day Tropical Bliss',
            category='Beach',
            description='Relax on the finest beaches in Bali.',
            duration_days=5,
            duration_nights=4,
            price=1000.00,
            discount_price=800.00,
            max_travelers=10,
            is_active=True
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bali Island')
        self.assertContains(response, 'Bali 5-Day Tropical Bliss')

    def test_destinations_list_and_detail(self):
        # List
        res_list = self.client.get(reverse('destinations_list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, 'Bali Island')

        # Detail
        res_detail = self.client.get(reverse('destination_detail', kwargs={'slug': self.destination.slug}))
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, 'Bali 5-Day Tropical Bliss')

    def test_packages_list_filtering(self):
        response = self.client.get(reverse('packages_list') + '?category=Beach')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bali 5-Day Tropical Bliss')

        # Filter by non-existent category
        response_empty = self.client.get(reverse('packages_list') + '?category=Mountain')
        self.assertEqual(response_empty.status_code, 200)
        self.assertNotContains(response_empty, 'Bali 5-Day Tropical Bliss')

    def test_package_detail_page(self):
        response = self.client.get(reverse('package_detail', kwargs={'slug': self.package.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '$800')

    def test_customer_booking_and_payment_flow(self):
        # Login customer
        self.client.login(username='customer_test', password='customerpassword123')

        # Step 1: Create booking
        booking_url = reverse('book_package', kwargs={'slug': self.package.slug})
        travel_date = timezone.now().date() + timedelta(days=15)
        
        post_data = {
            'contact_name': 'Alex Traveler',
            'contact_email': 'alex@travel.com',
            'contact_phone': '+1 555 123 4567',
            'travel_date': travel_date,
            'travelers_count': 2,
            'special_requests': 'Sea view room please'
        }
        res_book = self.client.post(booking_url, post_data)
        self.assertEqual(res_book.status_code, 302)

        booking = Booking.objects.filter(user=self.customer).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.travelers_count, 2)
        # 2 * 800 (discount price) = 1600
        self.assertEqual(booking.total_price, 1600.00)
        self.assertEqual(booking.status, 'Pending')

        # Step 2: Payment
        pay_url = reverse('process_payment', kwargs={'booking_number': booking.booking_number})
        res_pay = self.client.post(pay_url, {'payment_method': 'Credit Card'})
        self.assertEqual(res_pay.status_code, 302)

        # Verify booking confirmed & payment created
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Confirmed')
        payment = Payment.objects.filter(booking=booking).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.status, 'Completed')

    def test_admin_dashboard_security(self):
        # Customer cannot access admin dashboard
        self.client.login(username='customer_test', password='customerpassword123')
        res_cust = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_cust.status_code, 302)

        # Admin user CAN access
        self.client.login(username='admin_test', password='adminpassword123')
        res_admin = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_admin.status_code, 200)
        self.assertContains(res_admin, 'Tourism System Dashboard')

    def test_contact_form_submission(self):
        contact_url = reverse('contact_us')
        res = self.client.post(contact_url, {
            'name': 'Sarah Connor',
            'email': 'sarah@example.com',
            'phone': '1234567890',
            'subject': 'Inquiry about Bali Tour',
            'message': 'Can I book for a group of 8 people?'
        })
        self.assertEqual(res.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email='sarah@example.com').exists())
