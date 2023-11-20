from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Create order')
        user = User.objects.get(username='admin')
        products = Product.objects.all()
        order, created = Order.objects.get_or_create(
           user=user,
           delivery_address='Kazan, Bulgakov str. 8')

        for product in products:
            order.products.add(product)
        order.save()

        self.stdout.write(f'Created order {order}')