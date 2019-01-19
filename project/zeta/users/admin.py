# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

"""Define admin model for CustomUser model with no username field."""
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_type',
                                         'about', 'picture_url',)}),
        (_('Provider info'), {'fields': ('location', 'neighbourhood', 
                                         'provider_listings_count', 'provider_since',)}),
        (_('Visitor info'), {'fields': ('visitor_rating',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'identity_verified', 'groups',
                                       'user_permissions',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
