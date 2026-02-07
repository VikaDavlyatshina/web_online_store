from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProductForm
from .models import Category, Contact, Product

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
    login_url = '/users/login/'
    redirect_field_name = 'next'



class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания товара
    """
    model = Product
    template_name = "catalog/product_add.html"
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all().order_by("name")
        return context

    def get_success_url(self):
        """Редирект на страницу созданного товара"""
        return reverse("catalog:product_details", args=[self.object.pk])

     # Куда редиректить если не авторизован
    login_url = '/users/login/'
    redirect_field_name = 'next'

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
    login_url = '/users/login/'
    redirect_field_name = 'next'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для Удаления товара
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    # Куда редиректить если не авторизован
    login_url = '/users/login/'
    redirect_field_name = 'next'


class ContactsView(LoginRequiredMixin, TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts"] = Contact.objects.all().order_by("-created_at")

        # Проверяем сообщения из сессии (GET-запрос)
        if "contact_alert" in self.request.session:
            alert_data = self.request.session.pop("contact_alert")
            context["alert"] = {
                "type": alert_data["type"],
                "message": alert_data["message"],
            }
            if "form_data" in alert_data:
                context["form_data"] = alert_data["form_data"]

        return context

    def post(self, request, *args, **kwargs):
        # Обработка POST-запроса
        form_data = {
            "name": request.POST.get("name", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "message": request.POST.get("message", "").strip(),
        }

        try:
            contact = Contact(**form_data)
            contact.full_clean()
            contact.save()

            request.session["contact_alert"] = {
                "type": "success",
                "message": f"Спасибо, {contact.name}! Сообщение отправлено.",
            }

        except ValidationError as e:
            errors = []
            field_names = {"name": "Имя", "phone": "Телефон", "message": "Сообщение"}

            for field, name in field_names.items():
                if field in e.message_dict:
                    errors.append(f"{name}: {e.message_dict[field][0]}")

            if not errors and e.messages:
                errors = list(e.messages)

            error_text = f"Пожалуйста исправьте ошибки перед отправкой: {'; '.join(errors)}"

            request.session["contact_alert"] = {
                "type": "error",
                "message": error_text,
                "form_data": form_data,
            }

        return redirect(reverse("catalog:contacts"))

    # Куда редиректить если не авторизован
    login_url = '/users/login/'
    redirect_field_name = 'next'



