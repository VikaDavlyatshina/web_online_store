from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.cache import cache

from .forms import ProductForm, ContactForm, ProductModeratorForm
from .models import Contact, Product, Category
from .services import get_products_by_category


# Create your views here.


class ProductListView(ListView):
    """
    Представление для списка товаров с простым кешированием
    """

    model = Product
    context_object_name = 'products'
    ordering = ["-created_at"]
    paginate_by = 6

    def get_queryset(self):
        """
        Показываем товары в зависимости от пользователя с кешированием
        """
        user = self.request.user

        # Формируем ключ кеша в зависимости от пользователя
        if not user.is_authenticated:
            cache_key = "products_public"
        elif user.is_superuser or user.has_perm('catalog.can_unpublish_product'):
            cache_key = "products_all"
        else:
            cache_key = f"products_user_{user.id}"

        # Пробуем получить из кеша
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset

        queryset = super().get_queryset()

        # Применяем фильтры
        if not user.is_authenticated:
            filtered_queryset = queryset.filter(publication_status='published')
        elif user.is_superuser or user.has_perm('catalog.can_unpublish_product'):
            filtered_queryset = queryset  # все товары
        else:
            filtered_queryset = queryset.filter(
                Q(owner=user) |
                Q(publication_status='published')
            )

        # Сохраняем в кеш на 60 секунд
        cache.set(cache_key, filtered_queryset, 60)

        return filtered_queryset

class ProductDetailView(DetailView):  # Убрать LoginRequiredMixin
    """
    Представление для детального просмотра товара
    """
    model = Product
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        """Проверяем права на просмотр товара"""
        self.object = self.get_object()
        user = request.user

        if self.object.publication_status == 'published':
            # Опубликованные товары видят все
            return super().dispatch(request, *args, **kwargs)

        if user.is_authenticated:
            if (user == self.object.owner or
                    user.has_perm('catalog.can_unpublish_product') or
                    user.is_superuser):
                return super().dispatch(request, *args, **kwargs)

        # Если дошли сюда - нет прав на просмотр
        raise PermissionDenied

class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания товара
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_add.html"

    def form_valid(self, form):
        product = form.save(commit=False)  # Не сохраняем сразу
        product.owner = self.request.user
        product.publication_status = 'draft'  # Устанавливаем статус черновика
        product.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = None
        return context

    def get_success_url(self):
        """Редирект на страницу созданного товара"""
        return reverse("catalog:product_details", args=[self.object.pk])

    # Куда редиректить если не авторизован
    login_url = "/users/login/"
    redirect_field_name = "next"


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для Редактирования товара
    """

    model = Product

    def get_template_names(self):
        """Выбираем шаблон в зависимости от пользователя"""
        user = self.request.user
        product = self.get_object()

        # Если пользователь - модератор (но не владелец товара)
        if user.has_perm("catalog.can_unpublish_product") and user != product.owner:
            return ["catalog/product_moderator_edit.html"]

        # Для Владельца, суперпользователя и модератора-владельца
        return ["catalog/product_add.html"]

    def get_form_class(self):
        """Выбираем форму в зависимости от прав"""
        user = self.request.user
        product = self.get_object()

        # 1. Модератор (но НЕ владелец этого товара)
        if user.has_perm("catalog.can_unpublish_product") and user != product.owner:
            return ProductModeratorForm

        # 2. Суперпользователь или владелец (включая модератора-владельца)
        if user.is_superuser or user == product.owner:
            return ProductForm

        # 3. Нет прав
        raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        """Проверяем права на редактирование товара"""
        self.object = self.get_object()
        user = request.user

        # Может редактировать: владелец, модератор или суперпользователь
        can_edit = (
                user == self.object.owner or
                user.has_perm('catalog.can_unpublish_product') or
                user.is_superuser
        )

        if not can_edit:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Добавляем информацию о товаре для отображения"""
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object()  # Текущий товар
        return context

    def form_valid(self, form):
        """Обработка комментария модератора"""
        # Сохраняем комментарий в сессии или отправляем уведомление
        if 'moderator_comment' in form.cleaned_data and form.cleaned_data['moderator_comment']:
            comment = form.cleaned_data['moderator_comment']
            messages.info(self.request, f"Комментарий модератора сохранен: {comment}")

        return super().form_valid(form)

    def get_success_url(self):
        """Редирект на страницу созданного товара"""
        return reverse("catalog:product_details", args=[self.object.pk])

    # Куда редиректить если не авторизован
    login_url = "/users/login/"
    redirect_field_name = "next"


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для Удаления товара
    """

    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        """Проверяем права перед удалением"""
        self.object = self.get_object()
        user = request.user

        # Может удалять: владелец, модератор с правом удаления ИЛИ суперпользователь
        can_delete = (
                user == self.object.owner or
                user.has_perm('catalog.delete_product') or
                user.is_superuser
        )

        if not can_delete:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    # Куда редиректить если не авторизован
    login_url = "/users/login/"
    redirect_field_name = "next"

class CategoryProductView(ListView):
    """Представление для отображения продуктов в категории"""

    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        """Получаем queryset для товаров данной категории"""

        # Получаем ID категории из URL
        category_id = self.kwargs.get("category_id")

        # Используем сервисную функцию
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        """Добавляем дополнительную информацию в контекст"""

        context = super().get_context_data(**kwargs)

        # Получаем ID категории из URL
        category_id = self.kwargs.get("category_id")

        # Находим категорию для отображения названия
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category

        # Добавляем заголовок страницы
        context['title'] = f'Товары в категории: {category.name}'

        # Добавляем категории для бокового меню/ссылок
        context['categories'] = Category.objects.annotate(
            product_count=models.Count('products')
        ).filter(
            product_count__gt=0
        ).order_by('name')

        # Хлебные крошки для категории
        context['breadcrumbs'] = [
            {'name': 'Каталог', 'url': reverse('catalog:product_list')},
            {'name': category.name, 'url': ''},
        ]

        return context

class CategoryListView(ListView):
    """Представление для списка Категорий"""

    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        # Получаем категории с количеством товаров в каждой
        return Category.objects.annotate(
            product_count=models.Count('products')
        ).filter(
            product_count__gt=0  # Только категории, где есть товары
        ).order_by('name')

class ContactCreateView(LoginRequiredMixin, FormView):
    """
    Представление для страницы Контактов
    Автоматически обрабатывает GET и POST запросы
    """

    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")

    # Куда редиректить если не авторизован
    login_url = "/users/login/"
    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        """Добавляем список контактов в контекст"""

        context = super().get_context_data(**kwargs)
        context["contacts"] = Contact.objects.all().order_by("-created_at")
        return context

    def form_valid(self, form):
        """
        Вызывается, когда форма валидна.
        Автоматически сохраняет данные
        """

        # Сохраняем контакт в БД
        contact = form.save()

        # Добавляем сообщение об успехе
        messages.success(self.request, f"Спасибо, {contact.name}! Сообщение отправлено.")

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Вызывается, когда форма невалидна.
        Автоматически показывает ошибки в шаблоне
        """
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")

        return super().form_invalid(form)
