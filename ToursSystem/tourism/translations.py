"""
Khmer and English translation dictionary and helper functions.
Supports seamless dual-language switching for Wanderlust Tourism System.
"""

from django.utils.translation import get_language

TRANSLATIONS_KM = {
    # Navigation & Header
    "Home": "ទំព័រដើម",
    "Destinations": "គោលដៅទេសចរណ៍",
    "Tour Packages": "កញ្ចប់ទេសចរណ៍",
    "About Us": "អំពីយើង",
    "Contact": "ទំនាក់ទំនង",
    "Contact Us": "ទំនាក់ទំនងមកយើង",
    "Sign In": "ចូលគណនី",
    "Join Free": "ចុះឈ្មោះឥតគិតថ្លៃ",
    "Sign Out": "ចាកចេញ",
    "Admin Portal": "ផ្ទាំងគ្រប់គ្រងរដ្ឋបាល",
    "My Bookings & Profile": "ការកក់ និងប្រវត្តិរូប",
    "Management Dashboard": "ផ្ទាំងគ្រប់គ្រងទូទៅ",
    "Django Native Admin": "Django Admin",
    "Search": "ស្វែងរក",
    "Signed in as": "បានចូលគណនីជា",

    # Hero & Homepage
    "Discover The World's Most Extraordinary Journeys": "ស្វែងរកដំណើរកម្សាន្តដ៏អស្ចារ្យបំផុតលើពិភពលោក",
    "Handcrafted travel packages, unforgettable expeditions, and seamless luxury bookings tailored for you.": "កញ្ចប់ដំណើរកម្សាន្តដ៏ប្រណិត បទពិសោធន៍ដែលមិនអាចបំភ្លេចបាន និងការកក់ដ៏រហ័សទាន់ចិត្តសម្រាប់អ្នក។",
    "Explore Packages": "មើលកញ្ចប់ទេសចរណ៍",
    "All Categories": "ប្រភេទទាំងអស់",
    "All Destinations": "គោលដៅទាំងអស់",
    "Duration": "រយៈពេល",
    "Max Price": "តម្លៃអតិបរមា",
    "Find your dream tour": "ស្វែងរកដំណើរកម្សាន្តក្នុងក្តីស្រមៃរបស់អ្នក",
    "Featured Destinations": "គោលដៅទេសចរណ៍ល្បីៗ",
    "Hand-picked tourist spots for your next adventure": "ទីតាំងទេសចរណ៍ដែលពេញនិយមបំផុតសម្រាប់ការធ្វើដំណើររបស់អ្នក",
    "View All Destinations": "មើលគោលដៅទាំងអស់",
    "Trending Tour Packages": "កញ្ចប់ទេសចរណ៍ពេញនិយម",
    "Browse our highest rated and bestselling itineraries": "មើលកញ្ចប់ទេសចរណ៍ដែលទទួលបានការពេញចិត្តខ្ពស់បំផុត",
    "View Details": "មើលព័ត៌មានលម្អិត",
    "Book Now": "កក់ឥឡូវនេះ",
    "Book This Tour": "កក់ដំណើរកម្សាន្តនេះ",
    "Per Person": "ក្នុងម្នាក់",
    "per person": "ក្នុងម្នាក់",
    "/ person": "/ ម្នាក់",
    "Days": "ថ្ងៃ",
    "Nights": "យប់",
    "Day": "ថ្ងៃ",
    "Night": "យប់",
    "Rating": "ការវាយតម្លៃ",
    "Reviews": "ការវាយតម្លៃ",
    "reviews": "ការវាយតម្លៃ",

    # Stats
    "Global Destinations": "គោលដៅទេសចរណ៍សកល",
    "Curated Tour Packages": "កញ្ចប់ទេសចរណ៍សម្រិតសម្រាំង",
    "Happy Travelers": "ភ្ញៀវទេសចរពេញចិត្ត",
    "Guest Satisfaction": "ការពេញចិត្តរបស់ភ្ញៀវ",

    # Features / Value Props
    "Why Choose Wanderlust": "ហេតុអ្វីជ្រើសរើស Wanderlust",
    "Handcrafted Experiences": "បទពិសោធន៍សម្រិតសម្រាំងពិសេស",
    "Best Price Guarantee": "ការធានាតម្លៃសមរម្យបំផុត",
    "24/7 Concierge Support": "សេវាជំនួយអតិថិជន ២៤/៧",
    "Seamless Online Booking": "ការកក់ងាយស្រួលតាមអនឡាញ",
    "What Our Travelers Say": "មតិយោបល់ពីភ្ញៀវទេសចរ",
    "Verified Guest Reviews": "ការវាយតម្លៃពិតពីភ្ញៀវទេសចរ",

    # Categories
    "Adventure & Outdoors": "ផ្សងព្រេង និងធម្មជាតិ",
    "Beach & Coastal": "តំបន់ឆ្នេរ និងកោះ",
    "Cultural & Heritage": "វប្បធម៌ និងបេតិកភណ្ឌ",
    "Luxury & Wellness": "ភាពប្រណិត និងសុខុមាលភាព",
    "Wildlife & Safari": "សត្វព្រៃ និងព្រៃធម្មជាតិ",
    "Mountain & Hiking": "ឡើងភ្នំ និងដើរព្រៃ",
    "City Breaks & Sightseeing": "ទេសចរណ៍ទីក្រុង និងទស្សនាសម្ព័ន្ធ",
    "Adventure": "ផ្សងព្រេង",
    "Beach": "តំបន់ឆ្នេរ",
    "Cultural": "វប្បធម៌",
    "Luxury": "ប្រណិត",
    "Wildlife": "សត្វព្រៃ",
    "Mountain": "ភ្នំ",
    "City": "ទីក្រុង",

    # Package Detail Page
    "Overview": "ទិដ្ឋភាពទូទៅ",
    "Itinerary": "កាលវិភាគធ្វើដំណើរ",
    "What's Included": "អ្វីដែលរួមបញ្ចូល",
    "What's Excluded": "អ្វីដែលមិនរាប់បញ្ចូល",
    "Customer Reviews": "មតិយោបល់អតិថិជន",
    "Write a Review": "សរសេរមតិវាយតម្លៃ",
    "Your Rating": "ពិន្ទុរបស់អ្នក",
    "Your Comment": "មតិយោបល់របស់អ្នក",
    "Submit Review": "ផ្ញើមតិវាយតម្លៃ",
    "Group Size": "ទំហំក្រុម",
    "Max Travelers": "ចំនួនភ្ញៀវអតិបរមា",
    "Travel Style": "ទម្រង់ធ្វើដំណើរ",
    "Best Time": "ពេលវេលាល្អបំផុត",
    "Climate": "អាកាសធាតុ",
    "Related Tours": "ដំណើរកម្សាន្តស្រដៀងគ្នា",
    "Share This Tour": "ចែករំលែកដំណើរកម្សាន្តនេះ",

    # Booking & Payment
    "Book Tour Package": "កក់កញ្ចប់ទេសចរណ៍",
    "Booking Details": "ព័ត៌មានលម្អិតនៃការកក់",
    "Travel Date": "ថ្ងៃធ្វើដំណើរ",
    "Number of Travelers": "ចំនួនភ្ញៀវធ្វើដំណើរ",
    "Contact Information": "ព័ត៌មានទំនាក់ទំនង",
    "Full Name": "ឈ្មោះពេញ",
    "Email Address": "អាសយដ្ឋានអ៊ីមែល",
    "Phone Number": "លេខទូរស័ព្ទ",
    "Special Requests or Notes": "សំណើពិសេស ឬចំណាំបន្ថែម",
    "Proceed to Payment": "បន្តទៅការទូទាត់ប្រាក់",
    "Order Summary": "សង្ខេបការបញ្ជាទិញ",
    "Unit Price": "តម្លៃក្នុងម្នាក់",
    "Total Amount": "ចំនួនទឹកប្រាក់សរុប",
    "Total Price": "តម្លៃសរុប",
    "Subtotal": "សរុបរង",
    "Payment Checkout": "ការទូទាត់ប្រាក់",
    "Select Payment Method": "ជ្រើសរើសវិធីសាស្ត្រទូទាត់",
    "Credit / Debit Card": "កាតឥណទាន / ឥណពន្ធ",
    "Credit Card": "កាតឥណទាន",
    "PayPal": "PayPal",
    "Direct Bank Transfer": "ផ្ទេរប្រាក់តាមធនាគារ",
    "Cash on Arrival": "ទូទាត់ជាសាច់ប្រាក់ពេលមកដល់",
    "Card Number": "លេខកាត",
    "Cardholder Name": "ឈ្មោះម្ចាស់កាត",
    "Expiry Date": "កាលបរិច្ឆេទផុតកំណត់",
    "CVV / CVC": "CVV / CVC",
    "Pay Now": "ទូទាត់ប្រាក់ឥឡូវនេះ",
    "Booking Confirmation": "ការបញ្ជាក់ការកក់",
    "Booking Successful": "ការកក់ទទួលបានជោគជ័យ",
    "Booking Number": "លេខកូដការកក់",
    "Status": "ស្ថានភាព",
    "Payment Status": "ស្ថានភាពទូទាត់",
    "Transaction ID": "លេខកូដប្រតិបត្តិការ",
    "Print Voucher": "បោះពុម្ពប័ណ្ណកក់",
    "Return to Dashboard": "ត្រឡប់ទៅផ្ទាំងព័ត៌មាន",
    "Back to Home": "ត្រឡប់ទៅទំព័រដើម",

    # Statuses
    "Pending": "កំពុងរង់ចាំ",
    "Confirmed": "បានបញ្ជាក់",
    "Cancelled": "បានបោះបង់",
    "Completed": "បានបញ្ចប់",
    "Failed": "បរាជ័យ",
    "Refunded": "បានសងប្រាក់វិញ",
    "Pending Confirmation": "រង់ចាំការបញ្ជាក់",

    # Customer Dashboard
    "Customer Dashboard": "ផ្ទាំងព័ត៌មានអតិថិជន",
    "My Profile": "ប្រវត្តិរូបរបស់ខ្ញុំ",
    "Booking History": "ប្រវត្តិនៃការកក់",
    "Total Spent": "ទឹកប្រាក់ចំណាយសរុប",
    "Completed Trips": "ដំណើរកម្សាន្តដែលបានបញ្ចប់",
    "Active Bookings": "ការកក់សកម្ម",
    "Update Profile": "កែប្រែប្រវត្តិរូប",
    "First Name": "នាមខ្លួន",
    "Last Name": "នាមត្រកូល",
    "Address": "អាសយដ្ឋាន",
    "City": "ទីក្រុង",
    "Country": "ប្រទេស",
    "Profile Picture": "រូបថតប្រវត្តិរូប",
    "Save Changes": "រក្សាទុកការផ្លាស់ប្តូរ",
    "Cancel Booking": "បោះបង់ការកក់",
    "Action": "សកម្មភាព",
    "Actions": "សកម្មភាព",
    "View": "មើល",
    "Pay": "ទូទាត់",

    # Filter & Sort
    "Filter Packages": "ចម្រាញ់កញ្ចប់ទេសចរណ៍",
    "Sort By": "តម្រៀបតាម",
    "Popular": "ពេញនិយម",
    "Price: Low to High": "តម្លៃ: ទាបទៅខ្ពស់",
    "Price: High to Low": "តម្លៃ: ខ្ពស់ទៅទាប",
    "Duration: Short to Long": "រយៈពេល: ខ្លីទៅវែង",
    "Newest First": "ថ្មីបំផុតមុន",
    "Apply Filters": "អនុវត្តតម្រង",
    "Clear All": "សម្អាតទាំងអស់",
    "Showing": "កំពុងបង្ហាញ",
    "packages found": "កញ្ចប់ទេសចរណ៍ត្រូវបានរកឃើញ",
    "No tour packages found": "មិនមានកញ្ចប់ទេសចរណ៍ដែលត្រូវគ្នានោះទេ",

    # Destinations Page
    "Explore Destinations": "រុករកគោលដៅទេសចរណ៍",
    "Find your perfect getaway among world-class destinations": "ស្វែងរកដំណើរកម្សាន្តដ៏ល្អឥតខ្ចោះក្នុងចំណោមគោលដៅលំដាប់ពិភពលោក",
    "Search destination or country": "ស្វែងរកគោលដៅ ឬប្រទេស",
    "packages available": "កញ្ចប់ទេសចរណ៍មានផ្តល់ជូន",
    "package available": "កញ្ចប់ទេសចរណ៍មានផ្តល់ជូន",
    "Explore Tours": "មើលដំណើរកម្សាន្ត",

    # Contact Page & About Page
    "Get in Touch": "ទំនាក់ទំនងមកកាន់យើង",
    "We'd love to hear from you. Send our travel concierge team a message.": "យើងរីករាយក្នុងការផ្តល់ព័ត៌មានជូនលោកអ្នក។ សូមផ្ញើសារមកកាន់ក្រុមការងាររបស់យើង។",
    "Send Message": "ផ្ញើសារ",
    "Subject": "ប្រធានបទ",
    "Message": "ខ្លឹមសារសារ",
    "Our Office": "ការិយាល័យរបស់យើង",
    "Phone": "ទូរស័ព្ទ",
    "Email": "អ៊ីមែល",
    "Working Hours": "ម៉ោងធ្វើការ",
    "Mon - Sat: 8:00 AM - 6:00 PM": "ចន្ទ - សៅរ៍: ៨:០០ ព្រឹក - ៦:០០ ល្ងាច",
    "Sunday: Closed": "អាទិត្យ: សម្រាក",
    "About Wanderlust Journeys": "អំពី Wanderlust Journeys",

    # Admin Portal
    "Manager Portal": "ផ្ទាំងគ្រប់គ្រងរដ្ឋបាល",
    "Dashboard": "ផ្ទាំងព័ត៌មាន",
    "Bookings": "ការកក់",
    "Payments": "ការទូទាត់ប្រាក់",
    "Customers": "អតិថិជន",
    "Inquiries": "សារសាកសួរ",
    "Visit Public Site": "មើលគេហទំព័រ",
    "Administrator": "អ្នកគ្រប់គ្រង",
    "Add New": "បន្ថែមថ្មី",
    "Add New Destination": "បន្ថែមគោលដៅថ្មី",
    "Add New Tour Package": "បន្ថែមកញ្ចប់ទេសចរណ៍ថ្មី",
    "Edit": "កែប្រែ",
    "Delete": "លុប",
    "Total Bookings": "ការកក់សរុប",
    "Active Packages": "កញ្ចប់ទេសចរណ៍សកម្ម",
    "Total Customers": "អតិថិជនសរុប",
    "Recent Bookings": "ការកក់ថ្មីៗ",
    "Recent Inquiries": "សារសាកសួរថ្មីៗ",
    "Recent Messages": "សារថ្មីៗ",
    "Manage Destinations": "គ្រប់គ្រងគោលដៅទេសចរណ៍",
    "Manage Tour Packages": "គ្រប់គ្រងកញ្ចប់ទេសចរណ៍",
    "Manage Bookings": "គ្រប់គ្រងការកក់",
    "Manage Payments": "គ្រប់គ្រងការទូទាត់",
    "Manage Customers": "គ្រប់គ្រងអតិថិជន",
    "Manage Messages": "គ្រប់គ្រងសារ",
    "Booking Overview": "ទិដ្ឋភាពទូទៅនៃការកក់",
    "Revenue by Category": "ចំណូលតាមប្រភេទទេសចរណ៍",
    "Quick Actions": "សកម្មភាពរហ័ស",
    "Add Destination": "បន្ថែមគោលដៅ",
    "Add Package": "បន្ថែមកញ្ចប់",
    "View Bookings": "មើលការកក់",
    "View Payments": "មើលការទូទាត់",
    "Customer": "អតិថិជន",
    "Package": "កញ្ចប់ទេសចរណ៍",
    "Amount": "ចំនួនប្រាក់",
    "Date": "កាលបរិច្ឆេទ",
    "Method": "វិធីសាស្ត្រ",
    "Mark as Read": "សម្គាល់ថាបានអាន",
    "Mark as Unread": "សម្គាល់ថាមិនទាន់អាន",

    # Footer
    "Quick Links": "តំណភ្ជាប់រហ័ស",
    "Stay Connected": "ភ្ជាប់ទំនាក់ទំនង",
    "Subscribe to get seasonal private travel deals and secret discounts directly to your inbox.": "ជាវដើម្បីទទួលបានការបញ្ចុះតម្លៃពិសេស និងការផ្តល់ជូនថ្មីៗពីយើង។",
    "Enter your email": "បញ្ចូលអ៊ីមែលរបស់អ្នក",
    "24/7 Concierge": "សេវាជំនួយ ២៤/៧",
    "Privacy Policy": "គោលការណ៍ឯកជនភាព",
    "Terms of Service": "លក្ខខណ្ឌប្រើប្រាស់",
    "Security": "សុវត្ថិភាព",
    "All rights reserved.": "រក្សាសិទ្ធិគ្រប់យ៉ាង។",

    # Language Switcher
    "Language": "ភាសា",
    "English": "English",
    "Khmer": "ភាសាខ្មែរ",
}


def translate_text(text, lang=None):
    """
    Translates English text to Khmer if lang is 'km'.
    If lang is None, current active language is determined from request / session.
    """
    if lang is None:
        lang = get_language() or 'en'
    
    # Normalize language code (e.g. 'km-kh' -> 'km')
    lang = lang.lower().split('-')[0]

    if lang == 'km':
        clean_text = text.strip()
        if clean_text in TRANSLATIONS_KM:
            return TRANSLATIONS_KM[clean_text]
        # Case insensitive fallback
        lower_map = {k.lower(): v for k, v in TRANSLATIONS_KM.items()}
        if clean_text.lower() in lower_map:
            return lower_map[clean_text.lower()]
            
    return text
