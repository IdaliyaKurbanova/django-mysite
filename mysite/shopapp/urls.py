from django.urls import path
from .views import shop_index, products_list, orders_list, create_new_product, create_new_order

app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='index'),
    path('products/', products_list, name='products_list'),
    path('orders/', orders_list, name='orders_list'),
    path('create/product/', create_new_product, name='create_new_product'),
    path('create/order/', create_new_order, name='create_new_order'),
]
