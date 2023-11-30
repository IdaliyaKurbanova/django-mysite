from django.shortcuts import render, reverse, redirect
from django.http import HttpRequest
from typing import List, Dict, Any
from .models import Product, Order
from .forms import ProductForm, OrderForm


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


def create_new_product(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)

    else:
        form = ProductForm()
    context = {"form": form, }
    return render(request, 'shopapp/create-product.html', context=context)


def orders_list(request: HttpRequest):
    context: Dict[str, Any] = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)


def create_new_order(request: HttpRequest):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(delivery_address=form.cleaned_data["delivery_address"],
                                 promocode=form.cleaned_data["promocode"],
                                 user=form.cleaned_data["user"])
            for product in form.cleaned_data["products"]:
                order.products.add(product)
            order.save()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()
    context = {"form": form, }
    return render(request, 'shopapp/create-order.html', context=context)


