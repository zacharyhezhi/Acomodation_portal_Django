# users/urls.py
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('users/signup/', views.SignUp.as_view(), name='signup'),
    path('users/<int:user_id>/', views.profile, name='profile'),
    path('users/edit/<int:user_id>/', views.EditProfile.as_view(), name='edit'),
]
