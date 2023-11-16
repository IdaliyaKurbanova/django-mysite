from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.PositiveSmallIntegerField(default=0, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)


class Order(models.Model):
    delivery_address = models.TextField(blank=True, null=False)
    promocode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

