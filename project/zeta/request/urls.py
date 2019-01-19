# request/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'request'
urlpatterns = [
    path('place-a-request/', views.place_a_request, name='place-a-request'),
    path('place-a-request/controller', views.controller, name='controller'),
    path('place-a-request/place', views.place, name='01'),
    path('place-a-request/bedrooms', views.bedrooms, name='02'),
    path('place-a-request/bathrooms', views.bathrooms, name='03'),
    path('place-a-request/location', views.location, name='04'),
    path('place-a-request/amenities', views.amenities, name='05'),
    path('place-a-request/facilities', views.facilities, name='06'),
    path('place-a-request/description', views.description, name='07'),
    path('place-a-request/further-information', views.further_information, name='08'),
    
    path('manage-requests/', views.manage_requests, name='manage-requests'),
    path('request/<int:request_id>/', views.request_details, name='request-details'),
    path('request/edit/<int:request_id>/', views.EditRequest.as_view(), name='edit-request'),
    path('request/delete/<int:request_id>', views.delete_request, name='delete-request'),
    
    path('manage-bookings/', views.manage_bookings, name='manage-bookings'),
    path('booking/delete/<int:booking_id>', views.delete_booking, name='delete-booking'),
    path('booking/cancel/<int:booking_id>/<int:as_provider>', views.cancel_booking, name='cancel-booking'),
    path('booking/accept/<int:booking_id>', views.accept_booking, name='accept-booking'),
    path('booking/decline/<int:booking_id>', views.decline_booking, name='decline-booking'),
]
