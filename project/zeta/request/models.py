# request/models.py
from datetime import date, datetime

from django.db import models

from advertising.models import Listing
from users.models import CustomUser

class Request(models.Model):
    visitor       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    property_type = models.CharField(max_length=63, default='')
    room_type     = models.CharField(max_length=63, default='')

    accommodates  = models.PositiveSmallIntegerField(default=1)
    bedrooms      = models.PositiveSmallIntegerField(default=1)
    beds          = models.PositiveSmallIntegerField(default=1)
    bed_type      = models.CharField(max_length=31, null=True)

    bathrooms     = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    city          = models.CharField(max_length=63, default='')
    state         = models.CharField(max_length=63, default='')
    neighbourhood = models.CharField(max_length=63, default='')

    amenities     = models.CharField(max_length=2047, null=True)

    access        = models.CharField(max_length=1023, null=True)
    
    title         = models.CharField(max_length=255, default='')
    description   = models.CharField(max_length=1023, null=True)

    check_in      = models.DateField(default=date.today)
    check_out     = models.DateField(default=date.today)
    
    min_price     = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    max_price     = models.DecimalField(max_digits=9, decimal_places=2, null=True)

class Booking(models.Model):
    listing      = models.ForeignKey(Listing, on_delete=models.CASCADE)
    visitor      = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in     = models.DateField()
    check_out    = models.DateField()
    submitted_on = models.DateTimeField(default=datetime.now)
    BOOKING_STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('D', 'Declined'),
        ('C', 'Canceled'),
    )
    status       = models.CharField(max_length=1, choices=BOOKING_STATUS_CHOICES, default='P')
