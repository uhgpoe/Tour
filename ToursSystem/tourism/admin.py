from django.contrib import admin
from .models import (
    CustomerProfile, Destination, TourPackage, TourImage,
    Booking, Payment, Review, ContactMessage
)


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 2


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city', 'country')
    list_filter = ('country', 'created_at')


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'is_featured', 'best_time_to_visit', 'created_at')
    list_filter = ('is_featured', 'country')
    search_fields = ('name', 'city', 'country', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'category', 'price', 'discount_price', 'duration_days', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active', 'destination')
    search_fields = ('title', 'description', 'destination__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TourImageInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'user', 'package', 'travel_date', 'travelers_count', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'travel_date', 'created_at')
    search_fields = ('booking_number', 'user__username', 'contact_name', 'contact_email', 'package__title')
    readonly_fields = ('booking_number', 'created_at', 'updated_at')
    list_editable = ('status',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'payment_method', 'amount', 'status', 'payment_date')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('transaction_id', 'booking__booking_number', 'booking__user__username')
    readonly_fields = ('transaction_id', 'payment_date')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'package__title', 'comment')
    list_editable = ('is_approved',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
