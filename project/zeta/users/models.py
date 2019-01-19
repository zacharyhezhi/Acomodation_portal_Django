# users/models.py
"""
Reference:
https://github.com/django/django/blob/master/django/contrib/auth/models.py
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

"""Define model manager for CustomUser model with no username field."""
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

"""Define CustomUser model with no username field."""
class CustomUser(AbstractUser):
    username                = None
    email                   = models.EmailField(_('email address'), unique=True)
    is_provider             = models.BooleanField(_('is_provider'), default=False)
    is_visitor              = models.BooleanField(_('is_visitor'), default=True)
    provider_since          = models.DateTimeField(_('provider since'), null=True)
    location                = models.CharField(_('location'), max_length=255, blank=True)
    about                   = models.CharField(_('about'), max_length=16383, blank=True)
    picture_url             = models.CharField(_('picture url'), max_length=255, blank=True)
    neighbourhood           = models.CharField(_('neighbourhood'), max_length=63, blank=True)
    provider_listings_count = models.PositiveSmallIntegerField(_('provider listings count'), null=True)
    identity_verified       = models.BooleanField(_('identity verified'), default=False)
    visitor_rating          = models.DecimalField(_('visitor rating'), decimal_places=2, max_digits=3, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
