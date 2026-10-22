from django.urls import path
from . import views

urlpatterns = [
    # Language Switcher
    path('language/<str:lang_code>/', views.switch_language, name='switch_language'),

    # Public Pages
    path('', views.home, name='home'),
    path('destinations/', views.destinations_list, name='destinations_list'),
    path('destinations/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('packages/', views.packages_list, name='packages_list'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),

    # Auth & Customer Portal
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/', views.customer_dashboard, name='profile'),
    
    # Booking & Checkout
    path('packages/<slug:slug>/book/', views.book_package, name='book_package'),
    path('bookings/<str:booking_number>/pay/', views.process_payment, name='process_payment'),
    path('bookings/<str:booking_number>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('bookings/<str:booking_number>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('packages/<int:package_id>/review/', views.add_review, name='add_review'),

    # Admin Management Portal
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/destinations/', views.admin_destinations, name='admin_destinations'),
    path('admin-dashboard/destinations/add/', views.admin_destination_add, name='admin_destination_add'),
    path('admin-dashboard/destinations/<int:pk>/edit/', views.admin_destination_edit, name='admin_destination_edit'),
    path('admin-dashboard/destinations/<int:pk>/delete/', views.admin_destination_delete, name='admin_destination_delete'),
    
    path('admin-dashboard/packages/', views.admin_packages, name='admin_packages'),
    path('admin-dashboard/packages/add/', views.admin_package_add, name='admin_package_add'),
    path('admin-dashboard/packages/<int:pk>/edit/', views.admin_package_edit, name='admin_package_edit'),
    path('admin-dashboard/packages/<int:pk>/delete/', views.admin_package_delete, name='admin_package_delete'),

    path('admin-dashboard/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin-dashboard/bookings/<str:booking_number>/', views.admin_booking_detail, name='admin_booking_detail'),

    path('admin-dashboard/payments/', views.admin_payments, name='admin_payments'),
    path('admin-dashboard/customers/', views.admin_customers, name='admin_customers'),
    path('admin-dashboard/messages/', views.admin_messages, name='admin_messages'),
    path('admin-dashboard/messages/<int:pk>/toggle/', views.admin_message_toggle_read, name='admin_message_toggle_read'),
]
