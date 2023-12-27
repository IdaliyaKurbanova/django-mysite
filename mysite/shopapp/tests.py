from django.contrib.auth.models import User, Permission
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Order


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user, created = User.objects.get_or_create(username='John', password='qwerty')
        cls.permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(cls.permission)

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(user=self.user)

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_detail',
                                           kwargs={'pk': self.order.pk}))
        self.assertContains(response, 'Delivery_address')
        self.assertContains(response, 'Promocode')
        self.assertEqual(self.order.pk, response.context['order'].pk)

    def test_without_permission(self):
        user_permission = self.user.user_permissions.get(id=self.permission.id)
        user_permission.delete()
        self.client.get(reverse('shopapp:order_detail',
                                           kwargs={'pk': self.order.pk}))
        self.assertRaises(PermissionDenied)

    def tearDown(self):
        self.order.delete()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class OrdersExportTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user, created = User.objects.get_or_create(username='John', password='qwerty')
        cls.user.is_staff = True
        cls.user.save()

    def setUp(self):
        self.client.force_login(self.user)

    def test_export_orders(self):
        fixtures = ['orders-fixture.json', 'products-fixture.json', 'users-fixture.json']
        response = self.client.get(reverse('shopapp:orders_export'))
        expected_data = [{'ID': order.pk,
                          'Delivery_address': order.delivery_address,
                          'Promocode': order.promocode,
                          'User': str(order.user.pk),
                          'Products': [product.pk for product in order.products.all()]}
                         for order in Order.objects.all()]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['orders'], expected_data)

    def test_without_permission(self):
        self.user.is_staff = False
        self.user.save()
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 403)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
