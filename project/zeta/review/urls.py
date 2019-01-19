# request/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'review'
urlpatterns = [
    path('review/add', views.add_visitor_review, name='add-visitor-review'),
    path('review/delete/<int:review_id>/', views.delete_visitor_review, name='delete-visitor-review'),
    path('review/edit/<int:review_id>/', views.EditReview.as_view(), name='edit-visitor-review'),
]
