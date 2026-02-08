from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import ProductForm, ContactForm
from .models import Contact, Product

# Create your views here.


class ProductListView(ListView):
    """
    Представление для списка товаров
    """

    model = Product

    ordering = ["-created_at"]
    paginate_by = 6

    def get_queryset(self):
        """
        Переопределение метода.
        Выводятся только опубликованные статьи
        """

        return super().get_queryset().filter(is_published=True)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детального просмотра товара
    """

    model = Product
    context_object_name = "product"

    # Куда редиректить если не авторизован
    login_url = "/users/login/"
    redirect_field_name = "next"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания товара
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_add.html"

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    form_class = ProductForm
    template_name = "catalog/product_add.html"

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

    # Куда редиректить если не авторизован
    login_url = "/users/login/"
    redirect_field_name = "next"


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
