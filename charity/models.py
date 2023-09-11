from django.db import models
from django.utils import timezone


# Create your models here.


class Charity(models.Model):
    payment_Status = (
        (1, "Accepted"),
        (2, "Rejected"),
        (3, "Pending")
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    price = models.BigIntegerField(max_length=100, null=False, blank=False)
    phone_number=models.IntegerField(max_length=15, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=payment_Status, null=False, blank=False)
