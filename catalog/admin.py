from django.contrib import admin
from .models import Product, Category, Contact

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "purchase_price", "category")
    list_filter = ("category",)
    search_fields = (
        "name",
        "descriptions",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "created_at", )
    list_filter = ("created_at",)
    search_fields = (
        "name",
        "phone",
        "created_at"
    )

