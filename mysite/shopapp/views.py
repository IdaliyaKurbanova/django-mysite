from django.shortcuts import render, reverse, redirect
from django.http import HttpRequest, HttpResponseRedirect
from typing import List, Dict, Any

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Order
from .forms import ProductForm, OrderForm


def shop_index(request: HttpRequest):
    context: Dict[str, List[Dict[str]]] = {
    "menu": [{'title': "Products to order", 'url_name': 'shopapp:products_list'},
            {'title': "Current orders list", 'url_name': 'shopapp:orders_list'},],
                             }
    return render(request, 'shopapp/shopapp-index.html', context=context)


class ProductListView(ListView):
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "description", "price", "discount"
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "description", "price", "discount", "archived"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse('shopapp:product_detail', kwargs={"pk": self.object.pk})


class ProductArchiveView(DeleteView):
    model = Product
    template_name_suffix = "_confirm_archive"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('shopapp:product_detail', kwargs={"pk": self.object.pk})


class OrderListView(ListView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderDetailView(DetailView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreateView(CreateView):
    model = Order
    fields = "promocode", "user", "products", "delivery_address",
    success_url = reverse_lazy('shopapp:order_list')


class OrderUpdateView(UpdateView):
    model = Order
    template_name_suffix = "_update_form"
    fields = "promocode", "user", "products", "delivery_address",

    def get_success_url(self):
        return reverse('shopapp:order_detail', kwargs={"pk": self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:order_list')



