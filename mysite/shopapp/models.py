from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.PositiveSmallIntegerField(default=0, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

