from django.core.cache import cache
from django.db.models import Q

from catalog.models import Product


def get_products_by_category(category_id):
    """
    Получает все продукты указанной Категории с использованием кеширования
    """

    # Ключ для кеша (уникальный для каждой категории)
    cache_key = f"category_products_{category_id}"

    # Пробуем получить из кеша
    products = cache.get(cache_key)

    if products is not None:
        return products

    # Если нет в кеше - берём из БД
    products = Product.objects.filter(
        category_id=category_id,
        publication_status="published",   # Только опубликованные
    ).select_related("category").order_by("name")

    cache.set(cache_key, products)
    return products

def get_all_products(user=None):
    """
    Получает все продукты (товары) с учетом прав пользователя.
    Использует низкоуровневое кеширование
    """

    # Формируем ключ кеша в зависимости от пользователя
    if user and user.is_authenticated:
        if user.is_superuser or user.has_perm("catalog.can_unpublish_product"):
            cache_key = "all_product_moderator"
        else:
            cache_key = f"all_product_user_{user.id}"
    else:
        cache_key = "all_products_public"

    # Пробуем получить из кеша
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    # Если нет в кеше - получаем из БД
    queryset = Product.objects.all().select_related("category", "owner")

    # Применяем фильтры по правам
    if not user or not user.is_authenticated:
        queryset = queryset.filter(publication_status="published")
    elif user.is_superuser or user.has_perm("catalog.can_unpublish_product"):
        queryset = queryset.filter(Q(publication_status="published") | Q(owner=user))

    # Для модераторов и админов - все товары
    queryset = queryset.order_by('-created_at')

    # Кешируем на 5 минут
    cache.set(cache_key, queryset, 60)

    return queryset

