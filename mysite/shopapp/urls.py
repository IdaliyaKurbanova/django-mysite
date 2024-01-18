from django.urls import path, include
from .views import (shop_index,
                    ProductListView,
                    OrderListView,
                    ProductCreateView,
                    OrderCreateView,
                    ProductDetailView,
                    ProductUpdateView,
                    ProductArchiveView,
                    OrderDetailView,
                    OrderUpdateView,
                    OrderDeleteView,
                    OrdersExportView,
                    LatestProductsFeed
                    )
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)


app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='index'),
    path('api/', include(routers.urls)),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/latest/feed', LatestProductsFeed(), name='latest_products_feed'),
    path('products/create/', ProductCreateView.as_view(), name='create_new_product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('products//<int:pk>archive/', ProductArchiveView.as_view(), name='archive_product'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/create/', OrderCreateView.as_view(), name='create_new_order'),
    path('orders/export/', OrdersExportView.as_view(), name='orders_export'),
]
