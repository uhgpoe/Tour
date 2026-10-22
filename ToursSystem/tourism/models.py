from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class CustomerProfile(models.Model):
    """Extended customer profile linked to Django User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Destination(models.Model):
    """Tourist destination model."""
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Web image URL (fallback if file not uploaded)")
    best_time_to_visit = models.CharField(max_length=100, default='All Year Round')
    climate = models.CharField(max_length=100, default='Moderate / Sunny')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80'

    def __str__(self):
        return f"{self.name}, {self.country}"


class TourPackage(models.Model):
    """Tour package with details, pricing, itinerary, and inclusions."""
    CATEGORY_CHOICES = [
        ('Adventure', 'Adventure & Outdoors'),
        ('Beach', 'Beach & Coastal'),
        ('Cultural', 'Cultural & Heritage'),
        ('Luxury', 'Luxury & Wellness'),
        ('Wildlife', 'Wildlife & Safari'),
        ('Mountain', 'Mountain & Hiking'),
        ('City', 'City Breaks & Sightseeing'),
    ]

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Adventure')
    description = models.TextField()
    duration_days = models.PositiveIntegerField(default=3, help_text="Number of days")
    duration_nights = models.PositiveIntegerField(default=2, help_text="Number of nights")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per person ($)")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Discounted price per person ($)")
    featured_image = models.ImageField(upload_to='packages/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Web image URL (fallback)")
    max_travelers = models.PositiveIntegerField(default=12, help_text="Maximum group size")
    
    itinerary = models.TextField(
        blank=True,
        help_text="Separate days using line breaks. Format: 'Day 1: Title - Details'"
    )
    inclusions = models.TextField(
        blank=True,
        help_text="Comma-separated or newline-separated items included in the price"
    )
    exclusions = models.TextField(
        blank=True,
        help_text="Comma-separated or newline-separated items NOT included"
    )

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while TourPackage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        """Returns discount price if valid, else regular price."""
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.discount_price < self.price:
            savings = self.price - self.discount_price
            return int((savings / self.price) * 100)
        return 0

    @property
    def display_image(self):
        if self.featured_image:
            return self.featured_image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80'

    @property
    def average_rating(self):
        approved_reviews = self.reviews.filter(is_approved=True)
        if approved_reviews.exists():
            avg = approved_reviews.aggregate(models.Avg('rating'))['rating__avg']
            return round(avg, 1)
        return 5.0

    @property
    def reviews_count(self):
        return self.reviews.filter(is_approved=True).count()

    @property
    def itinerary_list(self):
        """Parses itinerary into structured list."""
        if not self.itinerary:
            return []
        items = []
        for line in self.itinerary.strip().split('\n'):
            line = line.strip()
            if line:
                if ':' in line:
                    parts = line.split(':', 1)
                    items.append({'day': parts[0].strip(), 'desc': parts[1].strip()})
                else:
                    items.append({'day': f"Day {len(items)+1}", 'desc': line})
        return items

    @property
    def inclusions_list(self):
        if not self.inclusions:
            return []
        lines = [line.strip().lstrip('-•* ') for line in self.inclusions.replace(',', '\n').split('\n') if line.strip()]
        return lines

    @property
    def exclusions_list(self):
        if not self.exclusions:
            return []
        lines = [line.strip().lstrip('-•* ') for line in self.exclusions.replace(',', '\n').split('\n') if line.strip()]
        return lines

    def __str__(self):
        return f"{self.title} (${self.current_price})"


class TourImage(models.Model):
    """Additional gallery images for tour packages."""
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='packages/gallery/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    caption = models.CharField(max_length=150, blank=True)

    @property
    def display_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ''


class Booking(models.Model):
    """Customer tour bookings."""
    STATUS_CHOICES = [
        ('Pending', 'Pending Confirmation'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    booking_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    travel_date = models.DateField()
    travelers_count = models.PositiveIntegerField(default=1)
    contact_name = models.CharField(max_length=150)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30)
    special_requests = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = f"TRV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.booking_number} - {self.package.title} ({self.status})"


class Payment(models.Model):
    """Payments for bookings."""
    METHOD_CHOICES = [
        ('Credit Card', 'Credit / Debit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Direct Bank Transfer'),
        ('Cash', 'Cash on Arrival'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=64, unique=True)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='Credit Card')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.transaction_id} - ${self.amount} ({self.status})"


class Review(models.Model):
    """Customer ratings and reviews for packages."""
    RATING_CHOICES = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} on {self.package.title} ({self.rating}★)"


class ContactMessage(models.Model):
    """Contact inquiries and feedback from visitors."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
