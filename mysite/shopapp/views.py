from django.shortcuts import render
from django.http import HttpRequest
from typing import List, Dict, Any
from .models import Product, Order


def shop_index(request: HttpRequest):
    context: Dict[str, List[Dict[str]]] = {
    "menu": [{'title': "Products to order", 'url_name': 'shopapp:products_list'},
            {'title': "Current orders list", 'url_name': 'shopapp:orders_list'},],
                             }
    return render(request, 'shopapp/shopapp-index.html', context=context)


def products_list(request: HttpRequest):
    context: Dict[str, Any] = {
    "products": Product.objects.all()
    }
    return render(request, 'shopapp/products-list.html', context=context)


def orders_list(request: HttpRequest):
    context: Dict[str, Any] = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)

