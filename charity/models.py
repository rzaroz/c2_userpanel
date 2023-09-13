from django.db import models
from django.utils import timezone


class GeneralDate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def jtime_updated_at(self):
        return jalali_converter(self.updated_at)

    def jtime_created_at(self):
        return jalali_converter(self.created_at)

    class Meta:
        abstract = True


class Charity(GeneralDate):
    PAYMENT_STATUS = (
        (1, "Accepted"),
        (2, "Rejected"),
        (3, "Pending")
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    price = models.PositiveBigIntegerField(null=False, blank=False)
    phone_number = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(choices=PAYMENT_STATUS, null=False, blank=False)
