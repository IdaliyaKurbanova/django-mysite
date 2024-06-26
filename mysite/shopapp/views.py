import logging
from django.core import serializers
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.shortcuts import render, reverse, redirect
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound, Http404, HttpResponse
from typing import List, Dict, Any
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend

log = logging.getLogger(__name__)


class LatestProductsFeed(Feed):
    title = 'Latest products of cosmetic shop in sale'
    description = 'Presents latest products, which are in sale at the moment'
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return Product.objects.filter(archived=False)

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('created_by')
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ['name', 'description', 'price']
    ordering_fields = ['name']


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('products')
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ['delivery_address', 'user', 'promocode']
    ordering_fields = ['delivery_address', 'created_at']


def shop_index(request: HttpRequest):
    context: Dict[str, List[Dict[str]]] = {
    "menu": [{'title': "Products to order", 'url_name': 'shopapp:products_list'},
            {'title': "Current orders list", 'url_name': 'shopapp:order_list'},],
                             }
    log.info('Logging for info-level is set')
    return render(request, 'shopapp/shopapp-index.html', context=context)


class ProductListView(LoginRequiredMixin, ListView):
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


class ProductDetailView(DetailView):
    queryset = Product.objects.prefetch_related('images')


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    model = Product
    fields = "name", "description", "price", "discount",
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return response


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def test_func(self):
        self.object = self.get_object()
        return (self.request.user.is_superuser
                or self.request.user.has_perm('shopapp.change_product')
                or (self.object.created_by == self.request.user))

    def form_valid(self, form):
        response = super().form_valid(form)
        images = form.files.getlist('images')
        for img in images:
            ProductImage.objects.create(image=img, product=self.object)
        return response

    def get_success_url(self):
        return reverse('shopapp:product_detail', kwargs={"pk": self.object.pk})



class ProductArchiveView(UserPassesTestMixin, DeleteView):
    model = Product
    template_name_suffix = "_confirm_archive"

    def test_func(self):
        self.object = self.get_object()
        return (self.request.user.is_superuser
                or self.request.user.has_perm('shopapp.change_product')
                or (self.object.created_by == self.request.user))

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('shopapp:product_detail', kwargs={"pk": self.object.pk})


class OrderListView(ListView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
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


class OrdersExportView(UserPassesTestMixin, View):

    def test_func(self):
        test_result = self.get_test_func()
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        data = {'orders': [{'ID': order.pk,
                          'Delivery_address': order.delivery_address,
                          'Promocode': order.promocode,
                          'User': order.user.pk,
                          'Products': [product.pk for product in order.products.all()]}
                          for order in Order.objects.all()]}
        return JsonResponse(data)


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_orders_list.html'

    def get_queryset(self):
        try:
            self.owner = User.objects.get(pk=self.kwargs['user_id'])
        except Exception:
            raise Http404
        queryset = Order.objects.filter(user=self.owner).prefetch_related("products")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


def user_orders_export(request: HttpRequest, user_id: int) -> HttpResponse:
    key_for_cache = 'user_{}_orders'.format(user_id)
    data = cache.get(key_for_cache)
    if data is None:
        try:
            owner = User.objects.get(pk=user_id)
        except Exception:
            raise Http404
        orders = Order.objects.filter(user=owner).order_by('pk').prefetch_related("products")
        data = serializers.serialize('json', orders)
        cache.set(key_for_cache, data, 120)
    return HttpResponse(data)






