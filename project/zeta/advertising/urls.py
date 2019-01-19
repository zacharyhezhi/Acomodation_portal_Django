# advertising/urls.py
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'advertising'
urlpatterns = [
    path('become-a-host/', views.become_a_host, name='become-a-host'),
    path('become-a-host/controller', views.controller, name='controller'),
    # Step 1: Start with the basics
    path('become-a-host/place', views.place, name='1-01'),
    path('become-a-host/bedrooms', views.bedrooms, name='1-02'),
    path('become-a-host/bathrooms', views.bathrooms, name='1-03'),
    path('become-a-host/location', views.location, name='1-04'),
    path('become-a-host/amenities', views.amenities, name='1-05'),
    path('become-a-host/spaces', views.spaces, name='1-06'),
    # Step 2: Set the scene
    path('become-a-host/photos', views.photos, name='2-01'),
    path('become-a-host/description', views.description, name='2-02'),
    path('become-a-host/title', views.title, name='2-03'),
    # Step 3: Get ready for guests
    path('become-a-host/guest-requirements', views.guest_requirements, name='3-01'),
    path('become-a-host/house-rules', views.house_rules, name='3-02'),
    path('become-a-host/review-guest-requirements', views.review_guest_requirements, name='3-03'),
    path('become-a-host/keep-calendar-up-to-date', views.keep_calendar_up_to_date, name='3-04'),
    path('become-a-host/availability-settings', views.availability_settings, name='3-05'),
    path('become-a-host/calendar', views.calendar, name='3-06'),
    path('become-a-host/price', views.price, name='3-07'),
    path('become-a-host/promotion', views.promotion, name='3-08'),
    path('become-a-host/additional-pricing', views.additional_pricing, name='3-09'),
    path('become-a-host/booking-scenarios', views.booking_scenarios, name='3-10'),
    path('become-a-host/local-laws', views.local_laws, name='3-11'),
    
    path('manage-listings/', views.manage_listings, name='manage-listings'),
    path('listing/<int:listing_id>/', views.listing_details, name='listing-details'),
    path('listing/edit/<int:listing_id>/', views.EditListing.as_view(), name='edit-listing'),
    path('listing/delete/<int:listing_id>/', views.delete_listing, name='delete-listing'),
]
