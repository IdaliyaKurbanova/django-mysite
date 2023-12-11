from django.urls import path
from .views import (shop_index,
                    ProductListView,
                    orders_list,
                    ProductCreateView,
                    create_new_order,
                    ProductDetailView,
                    ProductUpdateView,
                    ProductArchiveView)

app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='index'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='create_new_product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('products//<int:pk>archive/', ProductArchiveView.as_view(), name='archive_product'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/create/', create_new_order, name='create_new_order'),
]
