from django.core.management import BaseCommand
from shopapp.models import Product
from typing import List


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('create_products')
        products: List[tuple] = [('lipstick', 599, 0),
                ('eyeshadows', 999, 20),
                ('powder', 1199, 0),
                ('perfume', 2599, 0),
                ('eyeliner', 49, 0),
                ]
        for name, price, discount in products:
            product, created = Product.objects.get_or_create(
                name=name, price=price, discount=discount)
            self.stdout.write(f'Created product {product.name}')
        self.stdout.write(self.style.SUCCESS("Products created"))
