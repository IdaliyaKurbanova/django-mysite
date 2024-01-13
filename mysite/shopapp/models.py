from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

def get_image_path(instance: 'ProductImage', filename):
    return "products/product_{pk}/filename".format(pk=instance.product.pk, filename=filename)

class Product(models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=100, verbose_name=_('наименование'))
    description = models.TextField(null=False, blank=True, verbose_name=_('описание'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('цена'))
    discount = models.PositiveSmallIntegerField(default=0, blank=True, null=False, verbose_name=_('скидка'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    archived = models.BooleanField(default=False, verbose_name=_('архивирован ли товар'))
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1,
                                   verbose_name=_('пользователь, создавший товар'))

    def __str__(self) -> str:
        return f"Product {self.name!r}, pk={self.pk}"


class Order(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    delivery_address = models.TextField(blank=True, null=False, verbose_name=_('адрес доставки'))
    promocode = models.CharField(max_length=100, blank=True, verbose_name=_('использованный промокод'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('пользователь, создавший заказ'))
    products = models.ManyToManyField(Product, related_name='orders', verbose_name=_('товары в заказе'))

    def __str__(self) -> str:
        return f"Order by user {self.user}, pk={self.pk}"


class ProductImage(models.Model):
    image = models.ImageField(upload_to=get_image_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    description = models.TextField(blank=True, null=True)