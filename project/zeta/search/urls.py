# search/urls.py
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'search'
urlpatterns = [
    path('search/controller', views.controller, name='controller'),
    path('home', views.index, name='index'),
    path('search/listing', views.listing_results, name='listing-results'),
    path('search/request', views.request_results, name='request-results'),
]
