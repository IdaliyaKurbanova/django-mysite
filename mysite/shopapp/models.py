from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

def get_image_path(instance: 'ProductImage', filename):
    return "products/product_{pk}/filename".format(pk=instance.product.pk, filename=filename)

class Product(models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.PositiveSmallIntegerField(default=0, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

    def __str__(self) -> str:
        return f"Product {self.name!r}, pk={self.pk}"


class Order(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    delivery_address = models.TextField(blank=True, null=False)
    promocode = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self) -> str:
        return f"Order by user {self.user}, pk={self.pk}"


class ProductImage(models.Model):
    image = models.ImageField(upload_to=get_image_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    description = models.TextField(blank=True, null=True)