# users/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'location', 'about', 'neighbourhood',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'location', 'about', 'neighbourhood',)
