from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description="Archive selected products")
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
    list_display = "pk", "delivery_address", "promocode", "created_at", "by_user"
    list_display_links = "pk", "delivery_address"
    ordering = "pk",
    search_fields = "pk", "delivery_address", "by_user"

    def get_queryset(self, request: HttpRequest):
        return Order.objects.select_related("user").prefetch_related("products")

    def by_user(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username



