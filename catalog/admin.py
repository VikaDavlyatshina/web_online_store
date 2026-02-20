from django.contrib import admin, messages

from .models import Category, Contact, Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "purchase_price", "category", "publication_status", "owner")

    # По каким критериям можно фильтровать
    list_filter = ("category", "publication_status", "owner", "created_at")

    # Поиск по полям
    search_fields = ("name", "description", "owner__username")

    # Быстрое редактирование прямо в списке
    list_editable = ("publication_status",)

    # Элементов на странице
    list_per_page = 50

    # Массовые действия
    actions = [
        'publish_selected',
        'unpublish_selected',
        'send_to_moderation',
        'reject_selected'
    ]

    def publish_selected(self, request, queryset):
        updated = queryset.update(publication_status='published')
        self.message_user(
            request,
            f" {updated} товаров опубликовано!",
            messages.SUCCESS
        )

    publish_selected.short_description = "Опубликовать выбранные"

    def unpublish_selected(self, request, queryset):
        updated = queryset.update(publication_status='draft')
        self.message_user(
            request,
            f"{updated} товаров снято с публикации",
            messages.SUCCESS
        )

    unpublish_selected.short_description = "Снять с публикации"

    def send_to_moderation(self, request, queryset):
        updated = queryset.update(publication_status='pending')
        self.message_user(
            request,
            f"{updated} товаров отправлено на модерацию",
            messages.SUCCESS
        )

    send_to_moderation.short_description = "Отправить на модерацию"

    def reject_selected(self, request, queryset):
        updated = queryset.update(publication_status='rejected')
        self.message_user(
            request,
            f"{updated} товаров отклонено",
            messages.WARNING
        )

    reject_selected.short_description = "Отклонить выбранные"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_count")

    def product_count(self, obj):
        """Показывает количество товаров в категории"""
        return obj.products.count()

    product_count.short_description = "Количество товаров"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "phone", "email")
    readonly_fields = ("created_at",)  # Дата создания только для чтения



