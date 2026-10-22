from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid

from tourism.models import (
    CustomerProfile, Destination, TourPackage, TourImage,
    Booking, Payment, Review, ContactMessage
)


class Command(BaseCommand):
    help = 'Seeds database with sample tourism data, admin account, and demo traveler'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding...")

        # 1. Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@wanderlust.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        else:
            self.stdout.write("Admin user already exists.")

        # 2. Demo Traveler User
        demo_user, created = User.objects.get_or_create(
            username='traveler',
            defaults={
                'email': 'traveler@example.com',
                'first_name': 'Elena',
                'last_name': 'Rostova',
            }
        )
        if created:
            demo_user.set_password('traveler123')
            demo_user.save()
            if hasattr(demo_user, 'profile'):
                demo_user.profile.phone = '+1 (555) 987-6543'
                demo_user.profile.city = 'San Francisco'
                demo_user.profile.country = 'United States'
                demo_user.profile.save()
            self.stdout.write(self.style.SUCCESS("Created demo user: traveler / traveler123"))

        # 3. Create Destinations
        destinations_data = [
            {
                'name': 'Bali Tropical Paradise',
                'country': 'Indonesia',
                'city': 'Ubud & Seminyak',
                'description': 'Experience mystical temples, lush emerald rice terraces, world-class beach sunsets, vibrant spiritual culture, and tranquil luxury wellness sanctuaries in the heart of Indonesia.',
                'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80',
                'best_time_to_visit': 'April - October',
                'climate': 'Tropical Warm & Sunny (27°C - 31°C)',
                'is_featured': True,
            },
            {
                'name': 'Swiss Alps & Glaciers',
                'country': 'Switzerland',
                'city': 'Zermatt & Interlaken',
                'description': 'Soar through majestic snow-capped alpine peaks, crystal-clear glacial lakes, iconic cogwheel mountain trains, and picturesque Swiss chalets surrounded by pristine meadows.',
                'image_url': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80',
                'best_time_to_visit': 'June - Sept (Hiking) or Dec - March (Skiing)',
                'climate': 'Alpine Fresh (15°C - 24°C in summer)',
                'is_featured': True,
            },
            {
                'name': 'Santorini Caldera & Islands',
                'country': 'Greece',
                'city': 'Oia & Fira',
                'description': 'Whitewashed cliffside villas perched over azure waters, world-famous Aegean sunsets, volcanic black sand beaches, and authentic Mediterranean seafood dining.',
                'image_url': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=1200&q=80',
                'best_time_to_visit': 'May - October',
                'climate': 'Mediterranean Warm & Breeze (24°C - 30°C)',
                'is_featured': True,
            },
            {
                'name': 'Kyoto Ancient Heritage',
                'country': 'Japan',
                'city': 'Kyoto',
                'description': 'Walk among thousand-year-old crimson torii gates, peaceful Zen rock gardens, golden temples, tranquil bamboo groves, and timeless tea ceremony traditions.',
                'image_url': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80',
                'best_time_to_visit': 'March - May (Cherry Blossoms) or Oct - Nov (Autumn)',
                'climate': 'Temperate (16°C - 24°C)',
                'is_featured': True,
            },
            {
                'name': 'Serengeti & Great Migration',
                'country': 'Tanzania',
                'city': 'Arusha & Serengeti',
                'description': 'Witness the world’s greatest wildlife spectacle across untamed savannahs, with pride of lions, elephants, leopards, and millions of wildebeest under boundless African skies.',
                'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=80',
                'best_time_to_visit': 'July - October (Migration river crossings)',
                'climate': 'Semi-arid Warm (22°C - 28°C)',
                'is_featured': True,
            },
            {
                'name': 'Amalfi Coast Luxury Escape',
                'country': 'Italy',
                'city': 'Positano & Capri',
                'description': 'Dramatic pastel cliffside villages, vintage convertible drives along winding coastal roads, private yacht cruises around Capri sea caves, and Michelin-starred Italian cuisine.',
                'image_url': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=80',
                'best_time_to_visit': 'May - September',
                'climate': 'Sunny Mediterranean (25°C - 32°C)',
                'is_featured': False,
            },
        ]

        created_destinations = {}
        for d_data in destinations_data:
            dest, _ = Destination.objects.get_or_create(
                name=d_data['name'],
                defaults=d_data
            )
            created_destinations[dest.name] = dest

        self.stdout.write(self.style.SUCCESS(f"Populated {len(created_destinations)} destinations."))

        # 4. Create Tour Packages
        packages_data = [
            {
                'destination': created_destinations['Bali Tropical Paradise'],
                'title': '7-Day Magical Bali & Nusa Penida Island Expedition',
                'category': 'Beach',
                'description': 'Indulge in an enchanting journey blending luxury spa relaxation with thrill-seeking adventure. Explore Ubud sacred monkey forest, swim with gentle manta rays at Nusa Penida, witness cliffside Kecak fire dance in Uluwatu, and dine in candlelit beachfront seafood cafes.',
                'duration_days': 7,
                'duration_nights': 6,
                'price': 1299.00,
                'discount_price': 1099.00,
                'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80',
                'max_travelers': 12,
                'itinerary': (
                    "Day 1: Arrival in Denpasar - VIP Private Airport Transfer & Check-in at 5-Star Beach Villa in Seminyak\n"
                    "Day 2: Cultural Ubud Discovery - Tegalalang Rice Terraces, Coffee Plantation & Sacred Monkey Forest\n"
                    "Day 3: Sunrise Mount Batur Volcano Jeep Safari & Relaxing Natural Volcanic Hot Springs\n"
                    "Day 4: Fast Boat to Nusa Penida - Kelingking T-Rex Cliff, Broken Beach & Snorkeling with Manta Rays\n"
                    "Day 5: Spiritual Tirta Empul Water Temple Blessing & Traditional Balinese Cooking Class\n"
                    "Day 6: Majestic Uluwatu Sunset Temple & Spellbinding Fire Dance followed by Jimbaran Bay Seafood Dinner\n"
                    "Day 7: Leisure Morning, Souvenir Shopping & Departure Transfer"
                ),
                'inclusions': "5-Star Villa & Resort Accommodation, Daily Buffet Breakfast, Nusa Penida Private Speedboat, All Sanctuary & Temple Entry Tickets, Air-Conditioned Private Transport, English-speaking Certified Guide",
                'exclusions': "International Airfare, Alcoholic Drinks, Personal Travel Insurance, Discretionary Tips",
                'is_featured': True,
            },
            {
                'destination': created_destinations['Swiss Alps & Glaciers'],
                'title': '6-Day Alpine Wonders: Glacier Express & Matterhorn Summit',
                'category': 'Mountain',
                'description': 'Experience the pinnacle of European mountain beauty. Board the panoramic Glacier Express railway across legendary viaducts, stand face-to-face with the iconic Matterhorn in Zermatt, and cruise turquoise Lake Brienz.',
                'duration_days': 6,
                'duration_nights': 5,
                'price': 2490.00,
                'discount_price': 2250.00,
                'image_url': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80',
                'max_travelers': 10,
                'itinerary': (
                    "Day 1: Arrive Zurich - Scenic First-Class Train to Interlaken & Evening Lake Brienz Cruise\n"
                    "Day 2: Jungfraujoch 'Top of Europe' Alpine Summit & Ice Palace Exploration\n"
                    "Day 3: Board the world-famous Panoramic Glacier Express train to Zermatt\n"
                    "Day 4: Gornergrat Cogwheel Mountain Railway with breathtaking Matterhorn vistas\n"
                    "Day 5: Swiss Chocolate & Artisan Cheese Tasting Workshop in traditional chalet\n"
                    "Day 6: Morning Alpine Stroll & Return Train to Zurich Airport"
                ),
                'inclusions': "First-Class Swiss Travel Rail Pass, Boutique 4-Star Mountain Hotels, Daily Breakfast & 3 Alpine Fondue Dinners, Mountain Cogwheel Rail Passes, Luggage Transfers",
                'exclusions': "Flights, Mountain Gear Rental, Personal Shopping, Optional Helicopter Tours",
                'is_featured': True,
            },
            {
                'destination': created_destinations['Santorini Caldera & Islands'],
                'title': '5-Day Romantic Santorini Sunset & Caldera Yacht Cruise',
                'category': 'Luxury',
                'description': 'The quintessential romantic getaway. Stay in cliffside cave suites with infinity plunge pools facing the volcanic caldera, savor wine tastings at ancient vineyards, and sail on a luxury catamaran at golden hour.',
                'duration_days': 5,
                'duration_nights': 4,
                'price': 1650.00,
                'discount_price': 1480.00,
                'image_url': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=1200&q=80',
                'max_travelers': 8,
                'itinerary': (
                    "Day 1: Arrival Santorini - Welcome Champagne & Check-in to Cliffside Luxury Villa in Oia\n"
                    "Day 2: Guided Walking Tour of Fira & Oia with Professional Photography Session\n"
                    "Day 3: Private Sunset Catamaran Sailing with Swimming in Hot Springs & BBQ on board\n"
                    "Day 4: Ancient Akrotiri Ruins & Caldera Wine Tasting at Santo Wines\n"
                    "Day 5: Sunrise Over the Aegean & Private Airport Transfer"
                ),
                'inclusions': "Luxury Caldera Suite with Jacuzzi, Semi-private Luxury Catamaran Cruise with Dinner & Open Bar, 4 Boutique Winery Tastings, Private Airport Transfers",
                'exclusions': "Flights, Greek Stay City Tax, Extra Spa Treatments",
                'is_featured': True,
            },
            {
                'destination': created_destinations['Kyoto Ancient Heritage'],
                'title': '6-Day Timeless Kyoto: Temples, Geisha Districts & Bamboo Forest',
                'category': 'Cultural',
                'description': 'Immerse yourself into the serene heart of Japanese tradition. Savor authentic Kaiseki multi-course dinners, stroll the Arashiyama bamboo path at dawn, and explore golden Kinkaku-ji temple.',
                'duration_days': 6,
                'duration_nights': 5,
                'price': 1780.00,
                'discount_price': 1599.00,
                'image_url': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80',
                'max_travelers': 10,
                'itinerary': (
                    "Day 1: Arrive Kyoto via Shinkansen Bullet Train - Traditional Ryokan Check-in with Onsen Hot Springs\n"
                    "Day 2: Dawn Walk at Fushimi Inari-Taisha Shrine & Historic Sake Brewery District\n"
                    "Day 3: Kinkaku-ji (Golden Pavilion), Ryoan-ji Zen Rock Garden & Authentic Tea Ceremony\n"
                    "Day 4: Arashiyama Bamboo Grove, Tenryu-ji Temple & Sagano Scenic Romantic Train\n"
                    "Day 5: Gion Geisha District Evening Walking Tour & Multi-course Michelin-level Kaiseki Feast\n"
                    "Day 6: Nishiki Market Food Tour & Farewell Departure"
                ),
                'inclusions': "Traditional Luxury Ryokan Accommodation with Onsen, Authentic Kaiseki Dinners, Master Tea Ceremony Experience, English-speaking Licensed Historian Guide",
                'exclusions': "International Flights, Personal Purchases, Optional Kimono Rental",
                'is_featured': True,
            },
            {
                'destination': created_destinations['Serengeti & Great Migration'],
                'title': '7-Day Ultimate Big Five Safari: Serengeti & Ngorongoro Crater',
                'category': 'Wildlife',
                'description': 'An unmissable wildlife adventure of a lifetime. Track lions, leopards, rhinos, cheetahs, and vast herds across the endless plains of the Serengeti in open-top 4x4 Land Cruisers with luxury tented camps.',
                'duration_days': 7,
                'duration_nights': 6,
                'price': 3100.00,
                'discount_price': 2850.00,
                'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=80',
                'max_travelers': 6,
                'itinerary': (
                    "Day 1: Kilimanjaro Airport Arrival - Transfer to Luxury Safari Lodge in Arusha\n"
                    "Day 2: Tarangire National Park - Giant Baobab Trees & Massive Elephant Herds\n"
                    "Day 3: Journey to Central Serengeti - Afternoon Game Drive Tracking Big Cats\n"
                    "Day 4: Full Day Serengeti Game Safari - Great Migration Crossing Tracking & Bush Picnic\n"
                    "Day 5: Sunrise Hot Air Balloon Safari with Champagne Breakfast & Serengeti Plains\n"
                    "Day 6: Descend into UNESCO Ngorongoro Crater - Black Rhino Tracking & Flamingos\n"
                    "Day 7: Maasai Cultural Village Visit & Departure Flight"
                ),
                'inclusions': "Luxury Tented Lodges, All National Park & Crater Fees, Unlimited Game Drives in Custom 4x4 Land Cruiser with Pop-up Roof, All Meals (Full Board), Professional Safari Naturalist Guide",
                'exclusions': "International Airfare, Visa Fees, Driver-Guide Gratuity",
                'is_featured': True,
            },
            {
                'destination': created_destinations['Amalfi Coast Luxury Escape'],
                'title': '4-Day Amalfi Glamour: Positano, Ravello & Capri Yacht Cruise',
                'category': 'Luxury',
                'description': 'Bask in Italian elegance along the Mediterranean coastline. Sip Limoncello on sun-drenched terrace gardens in Ravello, cruise around the Faraglioni rock formations in Capri, and explore Positano cliffside boutiques.',
                'duration_days': 4,
                'duration_nights': 3,
                'price': 1450.00,
                'discount_price': 1350.00,
                'image_url': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=80',
                'max_travelers': 8,
                'itinerary': (
                    "Day 1: Naples Private Chauffeur Pickup - Scenic Drive to Positano 5-Star Hotel\n"
                    "Day 2: Private Riva Speedboat Day Cruise to Capri Island & Blue Grotto\n"
                    "Day 3: Ravello Cliffside Villa Rufolo Gardens & Traditional Lemon Grove Tasting\n"
                    "Day 4: Leisure Shopping in Positano & Chauffeur Transfer to Naples Airport"
                ),
                'inclusions': "5-Star Sea View Accommodations, Private Boat Tour to Capri with Prosecco, Luxury Chauffeur Mercedes Van, Breakfast Daily",
                'exclusions': "Flights, City Tourist Taxes, Personal Expenses",
                'is_featured': False,
            },
        ]

        created_packages = []
        for p_data in packages_data:
            pkg, _ = TourPackage.objects.get_or_create(
                title=p_data['title'],
                defaults=p_data
            )
            created_packages.append(pkg)

        self.stdout.write(self.style.SUCCESS(f"Populated {len(created_packages)} tour packages."))

        # 5. Create Sample Bookings & Payments
        # Booking 1: Confirmed
        booking1, b1_created = Booking.objects.get_or_create(
            user=demo_user,
            package=created_packages[0],
            travel_date=timezone.now().date() + timedelta(days=21),
            defaults={
                'travelers_count': 2,
                'contact_name': 'Elena Rostova',
                'contact_email': 'traveler@example.com',
                'contact_phone': '+1 (555) 987-6543',
                'special_requests': 'We prefer vegetarian meals and high-floor room with sunset view.',
                'total_price': created_packages[0].current_price * 2,
                'status': 'Confirmed',
            }
        )
        if b1_created:
            Payment.objects.create(
                booking=booking1,
                transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}",
                payment_method='Credit Card',
                amount=booking1.total_price,
                status='Completed'
            )

        # Booking 2: Pending
        booking2, b2_created = Booking.objects.get_or_create(
            user=demo_user,
            package=created_packages[1],
            travel_date=timezone.now().date() + timedelta(days=45),
            defaults={
                'travelers_count': 1,
                'contact_name': 'Elena Rostova',
                'contact_email': 'traveler@example.com',
                'contact_phone': '+1 (555) 987-6543',
                'special_requests': 'Window seat on Glacier Express train please.',
                'total_price': created_packages[1].current_price,
                'status': 'Pending',
            }
        )

        # Booking 3: Completed
        booking3, b3_created = Booking.objects.get_or_create(
            user=demo_user,
            package=created_packages[2],
            travel_date=timezone.now().date() - timedelta(days=30),
            defaults={
                'travelers_count': 2,
                'contact_name': 'Elena Rostova',
                'contact_email': 'traveler@example.com',
                'contact_phone': '+1 (555) 987-6543',
                'special_requests': 'Honeymoon anniversary trip setup.',
                'total_price': created_packages[2].current_price * 2,
                'status': 'Completed',
            }
        )
        if b3_created:
            Payment.objects.create(
                booking=booking3,
                transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}",
                payment_method='PayPal',
                amount=booking3.total_price,
                status='Completed'
            )

        # 6. Create Customer Reviews
        reviews_data = [
            {
                'user': demo_user,
                'package': created_packages[0],
                'rating': 5,
                'comment': 'Absolutely magnificent trip! The 5-star villa in Seminyak was breathtaking, and swimming alongside gentle manta rays at Nusa Penida was a bucket-list dream come true. Our guide Wayan was kind, knowledgeable, and punctual. 10/10!',
            },
            {
                'user': demo_user,
                'package': created_packages[2],
                'rating': 5,
                'comment': 'Our honeymoon in Santorini was perfection. The private caldera sunset catamaran cruise was the highlight of our vacation. Everything ran smoothly without any stress!',
            },
            {
                'user': demo_user,
                'package': created_packages[3],
                'rating': 5,
                'comment': 'The peace and spiritual depth of Kyoto exceeded all expectations. The morning bamboo grove walk and traditional tea ceremony with a master were unforgettable.',
            },
        ]

        for r_data in reviews_data:
            Review.objects.get_or_create(
                user=r_data['user'],
                package=r_data['package'],
                defaults={'rating': r_data['rating'], 'comment': r_data['comment'], 'is_approved': True}
            )

        # 7. Create Sample Inquiries
        messages_data = [
            {
                'name': 'Marcus Vance',
                'email': 'marcus.v@example.com',
                'phone': '+1 (415) 321-9876',
                'subject': 'Custom Safari Package for Family of 5',
                'message': 'Hello, we are planning a family trip to Tanzania in August with 3 teenagers. Can we customize the Serengeti safari itinerary to include an extra day at Lake Manyara?',
                'is_read': False,
            },
            {
                'name': 'Sophia Laurent',
                'email': 'sophia.laurent@paris.fr',
                'phone': '+33 6 12 34 56 78',
                'subject': 'Inquiry about Swiss Glacier Express Booking',
                'message': 'We want to book the 6-day Swiss Alps trip for our 25th wedding anniversary. Are the train seats in first class guaranteed with window views?',
                'is_read': True,
            },
        ]

        for m_data in messages_data:
            ContactMessage.objects.get_or_create(
                name=m_data['name'],
                email=m_data['email'],
                subject=m_data['subject'],
                defaults=m_data
            )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
        self.stdout.write("Credentials:")
        self.stdout.write("  Admin:    Username: 'admin'    | Password: 'admin123'")
        self.stdout.write("  Traveler: Username: 'traveler' | Password: 'traveler123'")
