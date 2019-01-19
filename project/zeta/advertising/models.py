# advertising/models.py
from django.db import models

from users.models import CustomUser

class Listing(models.Model):
    provider               = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    has_availability       = models.BooleanField(default=True)
    availability_30        = models.PositiveSmallIntegerField(default=30)
    availability_60        = models.PositiveSmallIntegerField(default=60)
    availability_90        = models.PositiveSmallIntegerField(default=90)
    availability_365       = models.PositiveSmallIntegerField(default=365)
    number_of_reviews      = models.PositiveSmallIntegerField(default=0)
    first_review           = models.DateField(null=True)
    last_review            = models.DateField(null=True)
    review_rating          = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    
    # Step 1: Start with the basics
    property_type          = models.CharField(max_length=63, default='')
    square_feet            = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    room_type              = models.CharField(max_length=63, default='')
    is_dedicated           = models.BooleanField(default=False)

    accommodates           = models.PositiveSmallIntegerField(default=1)
    bedrooms               = models.PositiveSmallIntegerField(null=True)
    beds                   = models.PositiveSmallIntegerField(null=True)
    bed_type               = models.CharField(max_length=31, null=True)

    bathrooms              = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    street                 = models.CharField(max_length=63, default='')
    unit                   = models.CharField(max_length=63, null=True)
    city                   = models.CharField(max_length=63, default='')
    state                  = models.CharField(max_length=63, default='')
    zipcode                = models.CharField(max_length=63, null=True)

    amenities              = models.CharField(max_length=2047, null=True)

    access                 = models.CharField(max_length=1023, null=True)

    # Step 2: Set the scene
    picture_url            = models.CharField(max_length=255, default='')

    summary                = models.CharField(max_length=1023, null=True)
    description            = models.CharField(max_length=1023, null=True)
    notes                  = models.CharField(max_length=1023, null=True)
    neighbourhood_overview = models.CharField(max_length=1023, null=True)
    transit                = models.CharField(max_length=1023, null=True)
    
    title                  = models.CharField(max_length=255, null=True)
    
    # Step 3: Get ready for guests
    requirements           = models.CharField(max_length=255, null=True)
    cancellation_policy    = models.CharField(max_length=63, default='')

    house_rules            = models.CharField(max_length=1023, null=True)

    advance_notice         = models.CharField(max_length=15, null=True)
    check_in_from          = models.CharField(max_length=7, null=True)
    check_in_to            = models.CharField(max_length=7, null=True)
    advance_booking        = models.CharField(max_length=31, null=True)
    minimum_nights         = models.PositiveSmallIntegerField()
    maximum_nights         = models.PositiveSmallIntegerField()
    instant_bookable       = models.BooleanField(default=False)
    
    daily_price            = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    special_offer          = models.BooleanField(default=False)
    
    weekly_price           = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    monthly_price          = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    security_deposit       = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    cleaning_fee           = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    extra_people           = models.DecimalField(max_digits=9, decimal_places=2, null=True)

class Calendar(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    days    = models.CharField(max_length=31)
    month   = models.PositiveSmallIntegerField()
    year    = models.PositiveSmallIntegerField()
