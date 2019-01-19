# review/models.py
from datetime import date

from django.db import models

from advertising.models import Listing
from users.models import CustomUser

class Review(models.Model):
    REVIEW_TYPE_CHOICES = (
        (0, 'Visitor review Listing'),
        (1, 'Provider review Visitor'),
    )
    review_type  = models.PositiveSmallIntegerField(choices=REVIEW_TYPE_CHOICES)
    provider     = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='provider_id')
    visitor      = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='visitor_id')
    listing      = models.ForeignKey(Listing, on_delete=models.CASCADE)
    rating       = models.DecimalField(max_digits=5, decimal_places=2)
    content      = models.CharField(max_length=4095)
    submitted_on = models.DateField(default=date.today)
