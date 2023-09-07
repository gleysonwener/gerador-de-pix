from django.db import models


class Order(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.CharField(max_length=8)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=8)
    cvv = models.CharField(max_length=3)
    pix_key = models.CharField(max_length=50, blank=True, null=True)
