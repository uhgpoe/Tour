from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import uuid
import json

from .models import (
    CustomerProfile, Destination, TourPackage, TourImage,
    Booking, Payment, Review, ContactMessage
)
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm,
    BookingForm, PaymentProcessForm, ReviewForm, ContactForm,
    DestinationForm, TourPackageForm, BookingUpdateStatusForm
)


from django.conf import settings
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme


# Helper: Check if user is staff/admin
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def switch_language(request, lang_code):
    """
    Switch active language between English ('en') and Khmer ('km').
    Saves preference to session and cookie, then safely redirects to previous page.
    """
    lang_code = lang_code.lower().split('-')[0]
    if lang_code not in ['en', 'km']:
        lang_code = 'en'

    # Save to session
    request.session['django_language'] = lang_code
    # request.session[translation.LANGUAGE_SESSION_KEY] = lang_code

    # Activate translation for current request
    translation.activate(lang_code)

    # Determine safe redirect target
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = '/'

    response = redirect(next_url)
    response.set_cookie(
        getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language'),
        lang_code,
        max_age=getattr(settings, 'LANGUAGE_COOKIE_AGE', 365 * 24 * 60 * 60),
        httponly=False,
        samesite='Lax'
    )
    return response


# ==========================================
# PUBLIC FRONTEND VIEWS
# ==========================================

def home(request):
    """Homepage with hero, search, featured destinations, popular packages, testimonials."""
    featured_destinations = Destination.objects.filter(is_featured=True)[:6]
    if not featured_destinations.exists():
        featured_destinations = Destination.objects.all()[:6]

    popular_packages = TourPackage.objects.filter(is_active=True).order_by('-is_featured', '-created_at')[:6]
    latest_reviews = Review.objects.filter(is_approved=True).select_related('user', 'package')[:6]

    # Stats for counter
    total_destinations = Destination.objects.count()
    total_packages = TourPackage.objects.filter(is_active=True).count()
    total_customers = User.objects.filter(is_staff=False).count() or 1200
    avg_rating = Review.objects.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg'] or 4.9

    categories = TourPackage.CATEGORY_CHOICES
    destinations = Destination.objects.all().order_by('name')

    context = {
        'featured_destinations': featured_destinations,
        'popular_packages': popular_packages,
        'latest_reviews': latest_reviews,
        'total_destinations': total_destinations,
        'total_packages': total_packages,
        'total_customers': total_customers,
        'avg_rating': round(avg_rating, 1),
        'categories': categories,
        'destinations': destinations,
    }
    return render(request, 'tourism/home.html', context)


def destinations_list(request):
    """Browse all destinations with search & filter."""
    query = request.GET.get('q', '').strip()
    destinations = Destination.objects.annotate(package_count=Count('packages'))

    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'destinations': destinations,
        'query': query,
    }
    return render(request, 'tourism/destinations_list.html', context)


def destination_detail(request, slug):
    """Destination detail page showing overview and packages in that destination."""
    destination = get_object_or_404(Destination, slug=slug)
    packages = destination.packages.filter(is_active=True)
    return render(request, 'tourism/destination_detail.html', {
        'destination': destination,
        'packages': packages,
    })


def packages_list(request):
    """Browse, filter, and search tour packages."""
    packages = TourPackage.objects.filter(is_active=True).select_related('destination')

    # Filter parameters
    query = request.GET.get('q', '').strip()
    destination_id = request.GET.get('destination', '')
    category = request.GET.get('category', '')
    duration = request.GET.get('duration', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'popular')

    if query:
        packages = packages.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(destination__name__icontains=query) |
            Q(destination__country__icontains=query)
        )

    if destination_id:
        packages = packages.filter(destination_id=destination_id)

    if category:
        packages = packages.filter(category=category)

    if duration:
        if duration == '1-3':
            packages = packages.filter(duration_days__lte=3)
        elif duration == '4-7':
            packages = packages.filter(duration_days__gte=4, duration_days__lte=7)
        elif duration == '8+':
            packages = packages.filter(duration_days__gte=8)

    if max_price:
        try:
            packages = packages.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sorting
    if sort_by == 'price_asc':
        packages = packages.order_by('price')
    elif sort_by == 'price_desc':
        packages = packages.order_by('-price')
    elif sort_by == 'duration':
        packages = packages.order_by('duration_days')
    elif sort_by == 'newest':
        packages = packages.order_by('-created_at')
    else:
        packages = packages.order_by('-is_featured', '-created_at')

    # Pagination: 9 per page
    paginator = Paginator(packages, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_destinations = Destination.objects.all().order_by('name')
    categories = TourPackage.CATEGORY_CHOICES

    context = {
        'page_obj': page_obj,
        'packages_count': packages.count(),
        'all_destinations': all_destinations,
        'categories': categories,
        'selected_query': query,
        'selected_destination': destination_id,
        'selected_category': category,
        'selected_duration': duration,
        'selected_max_price': max_price,
        'selected_sort': sort_by,
    }
    return render(request, 'tourism/packages_list.html', context)


def package_detail(request, slug):
    """Detailed view for a specific tour package with booking form and reviews."""
    package = get_object_or_404(TourPackage, slug=slug, is_active=True)
    reviews = package.reviews.filter(is_approved=True).select_related('user')
    related_packages = TourPackage.objects.filter(
        Q(destination=package.destination) | Q(category=package.category),
        is_active=True
    ).exclude(id=package.id)[:3]

    review_form = ReviewForm()

    context = {
        'package': package,
        'reviews': reviews,
        'related_packages': related_packages,
        'review_form': review_form,
    }
    return render(request, 'tourism/package_detail.html', context)


def about_us(request):
    """About us page."""
    return render(request, 'tourism/about_us.html')


def contact_us(request):
    """Contact page with contact form."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent successfully. Our travel specialists will contact you shortly.")
            return redirect('contact_us')
        else:
            messages.error(request, "Please check the form and fix the errors.")
    else:
        form = ContactForm()
    return render(request, 'tourism/contact_us.html', {'form': form})


# ==========================================
# AUTHENTICATION & CUSTOMER PORTAL
# ==========================================

def register_user(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Save additional profile phone if provided
            phone = form.cleaned_data.get('phone')
            if phone and hasattr(user, 'profile'):
                user.profile.phone = phone
                user.profile.save()

            messages.success(request, f"Welcome to Wanderlust Journeys, {user.first_name or user.username}! Your account has been created.")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'tourism/auth/register.html', {'form': form})


def login_user(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'tourism/auth/login.html', {'form': form})


@login_required
def logout_user(request):
    """User logout."""
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')


@login_required
def customer_dashboard(request):
    """Customer profile and booking history."""
    user = request.user
    profile = getattr(user, 'profile', None)
    bookings = Booking.objects.filter(user=user).select_related('package', 'payment')

    if request.method == 'POST':
        # Profile update
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        if profile:
            profile.phone = request.POST.get('phone', profile.phone)
            profile.address = request.POST.get('address', profile.address)
            profile.city = request.POST.get('city', profile.city)
            profile.country = request.POST.get('country', profile.country)
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect('customer_dashboard')

    context = {
        'user': user,
        'profile': profile,
        'bookings': bookings,
        'total_spent': bookings.filter(status='Confirmed').aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'completed_trips': bookings.filter(status='Completed').count(),
        'active_bookings': bookings.filter(status__in=['Pending', 'Confirmed']).count(),
    }
    return render(request, 'tourism/customer_dashboard.html', context)


# ==========================================
# TOUR BOOKING & PAYMENT FLOW
# ==========================================

@login_required
def book_package(request, slug):
    """Booking page for a specific package."""
    package = get_object_or_404(TourPackage, slug=slug, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            
            # Verify travel date is future
            if booking.travel_date <= timezone.now().date():
                messages.error(request, "Travel date must be at least tomorrow.")
                return render(request, 'tourism/booking_form.html', {'package': package, 'form': form})

            # Calculate total price
            booking.total_price = booking.travelers_count * package.current_price
            booking.status = 'Pending'
            booking.save()

            messages.success(request, f"Booking #{booking.booking_number} created! Please complete payment to confirm your reservation.")
            return redirect('process_payment', booking_number=booking.booking_number)
        else:
            messages.error(request, "Please correct the errors in the booking form.")
    else:
        initial_data = {
            'contact_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'contact_email': request.user.email,
            'contact_phone': getattr(request.user.profile, 'phone', '') if hasattr(request.user, 'profile') else '',
            'travelers_count': 1,
            'travel_date': timezone.now().date() + timezone.timedelta(days=7),
        }
        form = BookingForm(initial=initial_data)

    return render(request, 'tourism/booking_form.html', {
        'package': package,
        'form': form
    })


@login_required
def process_payment(request, booking_number):
    """Payment checkout page for a booking."""
    booking = get_object_or_404(Booking, booking_number=booking_number, user=request.user)

    if booking.status in ['Confirmed', 'Completed']:
        messages.info(request, "This booking has already been paid and confirmed.")
        return redirect('booking_confirmation', booking_number=booking.booking_number)

    if request.method == 'POST':
        form = PaymentProcessForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            
            # Generate simulated transaction id
            tx_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"

            # Create or update Payment
            Payment.objects.update_or_create(
                booking=booking,
                defaults={
                    'transaction_id': tx_id,
                    'payment_method': payment_method,
                    'amount': booking.total_price,
                    'status': 'Completed',
                }
            )

            # Update booking status to Confirmed
            booking.status = 'Confirmed'
            booking.save()

            messages.success(request, "Payment successful! Your booking has been confirmed.")
            return redirect('booking_confirmation', booking_number=booking.booking_number)
    else:
        form = PaymentProcessForm(initial={'payment_method': 'Credit Card'})

    return render(request, 'tourism/payment_page.html', {
        'booking': booking,
        'form': form
    })


@login_required
def booking_confirmation(request, booking_number):
    """Receipt / Voucher / Confirmation page for a booking."""
    booking = get_object_or_404(Booking, booking_number=booking_number, user=request.user)
    payment = getattr(booking, 'payment', None)

    return render(request, 'tourism/booking_confirmation.html', {
        'booking': booking,
        'payment': payment
    })


@login_required
def cancel_booking(request, booking_number):
    """Cancel a booking by customer."""
    booking = get_object_or_404(Booking, booking_number=booking_number, user=request.user)
    if booking.status in ['Pending', 'Confirmed']:
        booking.status = 'Cancelled'
        booking.save()
        messages.warning(request, f"Booking #{booking.booking_number} has been cancelled.")
    else:
        messages.error(request, "This booking cannot be cancelled.")
    return redirect('customer_dashboard')


@login_required
def add_review(request, package_id):
    """Submit a review for a package."""
    package = get_object_or_404(TourPackage, id=package_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.package = package
            review.is_approved = True
            review.save()
            messages.success(request, "Thank you! Your review has been published.")
        else:
            messages.error(request, "Could not submit review. Please try again.")
    return redirect('package_detail', slug=package.slug)


# ==========================================
# ADMIN MANAGEMENT DASHBOARD
# ==========================================

@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    """Comprehensive Admin Dashboard with analytics, revenue charts, and quick actions."""
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='Pending').count()
    confirmed_bookings = Booking.objects.filter(status='Confirmed').count()
    completed_bookings = Booking.objects.filter(status='Completed').count()
    cancelled_bookings = Booking.objects.filter(status='Cancelled').count()

    total_revenue = Payment.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
    total_packages = TourPackage.objects.count()
    total_destinations = Destination.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()

    recent_bookings = Booking.objects.select_related('user', 'package').order_by('-created_at')[:6]
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]

    # Chart 1: Status distribution data
    status_chart_data = {
        'labels': ['Confirmed', 'Pending', 'Completed', 'Cancelled'],
        'data': [confirmed_bookings, pending_bookings, completed_bookings, cancelled_bookings]
    }

    # Chart 2: Revenue breakdown per category
    category_revenue = TourPackage.objects.filter(bookings__status__in=['Confirmed', 'Completed']).values('category').annotate(
        total_rev=Sum('bookings__total_price')
    ).order_by('-total_rev')

    cat_labels = [item['category'] for item in category_revenue] or ['Adventure', 'Beach', 'Cultural', 'Luxury']
    cat_values = [float(item['total_rev']) for item in category_revenue] or [3500, 4800, 2200, 6100]

    category_chart_data = {
        'labels': cat_labels,
        'data': cat_values
    }

    context = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'total_revenue': total_revenue,
        'total_packages': total_packages,
        'total_destinations': total_destinations,
        'total_customers': total_customers,
        'unread_messages': unread_messages,
        'recent_bookings': recent_bookings,
        'recent_messages': recent_messages,
        'status_chart_json': json.dumps(status_chart_data),
        'category_chart_json': json.dumps(category_chart_data),
    }
    return render(request, 'admin_panel/dashboard.html', context)


# Admin: Destination CRUD
@user_passes_test(is_admin, login_url='login')
def admin_destinations(request):
    destinations = Destination.objects.annotate(package_count=Count('packages')).order_by('-created_at')
    return render(request, 'admin_panel/destinations.html', {'destinations': destinations})


@user_passes_test(is_admin, login_url='login')
def admin_destination_add(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save()
            messages.success(request, f"Destination '{destination.name}' added successfully.")
            return redirect('admin_destinations')
    else:
        form = DestinationForm()
    return render(request, 'admin_panel/destination_form.html', {'form': form, 'title': 'Add New Destination'})


@user_passes_test(is_admin, login_url='login')
def admin_destination_edit(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, f"Destination '{destination.name}' updated successfully.")
            return redirect('admin_destinations')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'admin_panel/destination_form.html', {'form': form, 'title': f'Edit Destination: {destination.name}', 'destination': destination})


@user_passes_test(is_admin, login_url='login')
def admin_destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    name = destination.name
    destination.delete()
    messages.warning(request, f"Destination '{name}' has been deleted.")
    return redirect('admin_destinations')


# Admin: Package CRUD
@user_passes_test(is_admin, login_url='login')
def admin_packages(request):
    packages = TourPackage.objects.select_related('destination').annotate(booking_count=Count('bookings')).order_by('-created_at')
    return render(request, 'admin_panel/packages.html', {'packages': packages})


@user_passes_test(is_admin, login_url='login')
def admin_package_add(request):
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save()
            messages.success(request, f"Tour package '{package.title}' created successfully.")
            return redirect('admin_packages')
    else:
        form = TourPackageForm()
    return render(request, 'admin_panel/package_form.html', {'form': form, 'title': 'Add New Tour Package'})


@user_passes_test(is_admin, login_url='login')
def admin_package_edit(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, f"Tour package '{package.title}' updated successfully.")
            return redirect('admin_packages')
    else:
        form = TourPackageForm(instance=package)
    return render(request, 'admin_panel/package_form.html', {'form': form, 'title': f'Edit Package: {package.title}', 'package': package})


@user_passes_test(is_admin, login_url='login')
def admin_package_delete(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    title = package.title
    package.delete()
    messages.warning(request, f"Tour package '{title}' has been deleted.")
    return redirect('admin_packages')


# Admin: Bookings Management
@user_passes_test(is_admin, login_url='login')
def admin_bookings(request):
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.select_related('user', 'package', 'payment').order_by('-created_at')

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'admin_panel/bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter,
    })


@user_passes_test(is_admin, login_url='login')
def admin_booking_detail(request, booking_number):
    booking = get_object_or_404(Booking, booking_number=booking_number)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to '{new_status}'.")
            return redirect('admin_booking_detail', booking_number=booking.booking_number)

    return render(request, 'admin_panel/booking_detail.html', {'booking': booking})


# Admin: Payments & Reports
@user_passes_test(is_admin, login_url='login')
def admin_payments(request):
    payments = Payment.objects.select_related('booking', 'booking__user', 'booking__package').order_by('-payment_date')
    total_revenue = payments.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'admin_panel/payments.html', {
        'payments': payments,
        'total_revenue': total_revenue,
    })


# Admin: Customers Management
@user_passes_test(is_admin, login_url='login')
def admin_customers(request):
    customers = User.objects.filter(is_staff=False).annotate(
        booking_count=Count('bookings'),
        total_spent=Sum('bookings__total_price')
    ).order_by('-date_joined')
    return render(request, 'admin_panel/customers.html', {'customers': customers})


# Admin: Messages & Inquiries
@user_passes_test(is_admin, login_url='login')
def admin_messages(request):
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/messages.html', {'contact_messages': contact_messages})


@user_passes_test(is_admin, login_url='login')
def admin_message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save()
    status_str = "read" if msg.is_read else "unread"
    messages.info(request, f"Message marked as {status_str}.")
    return redirect('admin_messages')
