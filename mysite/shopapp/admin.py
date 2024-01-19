from csv import DictReader
from io import TextIOWrapper
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import path
from django.db import transaction

from .models import Product, Order
from .forms import CSVFileForm
from django.utils.translation import gettext_lazy as _


@transaction.atomic
def import_orders_from_csv(csv_file):
    """
    Данная функция проверяет корректность данных в csv-файле для создания заказа.
    Если указано некорректное имя пользователя или название продукта в заказе,
    или такой пользователь/продукт не существуют в базе данных, то такой заказ не создается.

    :param csv_file: csv-файл, заказы из которого необходимо загрузить в базу данных.
    :return: unsuccessful: Список порядковых номеров заказов из файла csv, которые не были созданы.
    """
    unsuccessful = []
    rows_count = 0
    users_names = [user['username'] for user in (User.objects.values('username').all())]
    products_names = [product['name'] for product in (Product.objects.values('name').all())]
    for row in DictReader(csv_file):
        rows_count += 1
        if row['username'] in users_names and row['product'] in products_names:
            user_pk = User.objects.get(username=row['username'])
            product_pk = Product.objects.get(name=row['product'])
            order, created = Order.objects.get_or_create(
                delivery_address=row['delivery_address'],
                promocode=row['promocode'],
                user=user_pk
            )
            order.products.add(product_pk)
            order.save()
        else:
            unsuccessful.append(rows_count)
    return unsuccessful


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description=_("Archive selected products"))
def mark_as_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [mark_as_archived]
    inlines = OrderInline,
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name",
    ordering = "pk",
    search_fields = "name", "description", "price"
    fieldsets = [
        (None, {"fields": ("name", "description")}),
        ("Price details", {"fields": ("price", "discount")}),
        ("Additional", {"fields": ("archived", ),
                        "classes": ("collapse",)})
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 30:
            return obj.description
        return obj.description[:30] + "..."



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"
    list_display = "pk", "delivery_address", "promocode", "created_at", "user_by"
    list_display_links = "pk", "delivery_address"
    ordering = "pk",
    search_fields = "pk", "delivery_address", "by_user"

    def get_queryset(self, request: HttpRequest):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_by(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_CSV(self, request: HttpRequest) -> HttpResponse:
        """
        Данный метод предназначен для импорта csv-файла с заказами.
        В случае, если request-метод GET, то рендерится страница с формой для загрузки файла.
        Аналогичный результат (только со статусом 400) возвращается,
        если форма после загрузки файла невалидна.
        При методе POST вызывается функция "import_orders_from_csv" (куда передается загруженный файл),
        которая возвращает переменную unsuccessful c номерами заказов в файле csv, которые не были созданы.
        Результаты создания заказов в виде сообщения пользователю отражаются на странице редиректа.

        :param request: HttpRequest
        :return: HttpResponse
        """
        if request.method == "GET":
            form = CSVFileForm()
            return render(request, 'admin/csv_form.html', {'form': form})

        form = CSVFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'admin/csv_form.html', {'form': form}, status=400)

        csv_file = TextIOWrapper(form.files['csv_file'].file)
        unsuccessful = import_orders_from_csv(csv_file)
        if not unsuccessful:
            self.message_user(request, message='All orders from csv-file were successfully uploaded')
        else:
            unsuccessful = ", ".join([str(row) for row in unsuccessful])
            self.message_user(request, message=f'Orders in row/rows #{unsuccessful} were not uploaded. \n'
                                               f'Incorrect values for username or product')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('import-csv', self.import_CSV, name='import_csv')]
        return new_urls + urls




