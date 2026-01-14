from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from .models import Product, Contact, Category
from django.views.generic import ListView, DetailView, TemplateView, FormView, CreateView


# Create your views here.


class ProductListView(ListView):
    model = Product

    ordering = ["-created_at"]
    paginate_by = 6


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all().order_by("-created_at")

        # Проверяем сообщения из сессии (GET-запрос)
        if 'contact_alert' in self.request.session:
            alert_data = self.request.session.pop('contact_alert')
            context['alert'] = {
                'type': alert_data['type'],
                'message': alert_data['message']
            }
            if 'form_data' in alert_data:
                context['form_data'] = alert_data['form_data']

        return context

    def post(self, request, *args, **kwargs):
        # Обработка POST-запроса
        form_data = {
            'name': request.POST.get("name", "").strip(),
            'phone': request.POST.get("phone", "").strip(),
            'message': request.POST.get("message", "").strip()
        }

        try:
            contact = Contact(**form_data)
            contact.full_clean()
            contact.save()

            request.session['contact_alert'] = {
                'type': 'success',
                'message': f"Спасибо, {contact.name}! Сообщение отправлено.",
            }

        except ValidationError as e:
            errors = []
            field_names = {'name': 'Имя', 'phone': 'Телефон', 'message': 'Сообщение'}

            for field, name in field_names.items():
                if field in e.message_dict:
                    errors.append(f"{name}: {e.message_dict[field][0]}")

            if not errors and e.messages:
                errors = list(e.messages)

            error_text = f"Пожалуйста исправьте ошибки перед отправкой: {'; '.join(errors)}"

            request.session['contact_alert'] = {
                'type': 'error',
                'message': error_text,
                'form_data': form_data
            }

        return redirect(reverse('catalog:contacts'))


# def contacts(request):
#     """Контроллер страницы Контактов"""
#
#     # Базовый контекст
#     context = {
#         'contacts': Contact.objects.all().order_by("-created_at")
#     }
#
#     # Обработка POST-запроса (отправка формы)
#     if request.method == "POST":
#         # Получаем данные из формы
#         form_data = {
#             'name': request.POST.get("name", "").strip(),
#             'phone': request.POST.get("phone", "").strip(),
#             'message': request.POST.get("message", "").strip()
#         }
#
#         try:
#             # Создаем и валидируем контакт
#             contact = Contact(**form_data)
#             contact.full_clean()
#             contact.save()
#
#             # Успешное сообщение
#             request.session['contact_alert'] = {
#                 'type': 'success',
#                 'message': f"Спасибо, {contact.name}! Сообщение отправлено.",
#             }
#
#         except ValidationError as e:
#             # Формируем сообщения об ошибках
#             errors = []
#             field_names = {'name': 'Имя', 'phone': 'Телефон', 'message': 'Сообщение'}
#
#             for field, name in field_names.items():
#                 if field in e.message_dict:
#                     errors.append(f"{name}: {e.message_dict[field][0]}")
#
#             if not errors and e.messages:
#                 errors = list(e.messages)
#
#             # Формируем итоговое сообщение
#             if errors:
#                 error_text = f"Пожалуйста исправьте ошибки перед отправкой: {'; '.join(errors)}"
#             else:
#                 error_text = "Произошла ошибка при отправке сообщения"
#
#             # Сообщение об ошибке
#             request.session['contact_alert'] = {
#                 'type': 'error',
#                 'message': error_text,
#                 'form_data': form_data
#             }
#
#         # Редирект после POST
#         return redirect(reverse('catalog:contacts'))
#
#     # Обработка GET-запроса (отображение страницы)
#
#     # Проверяем сообщения из сессии
#     if 'contact_alert' in request.session:
#         alert_data = request.session.pop('contact_alert')
#
#         context['alert'] = {
#             'type': alert_data['type'],
#             'message': alert_data['message']
#         }
#
#         # Восстанавливаем данные формы
#         if 'form_data' in alert_data:
#             context['form_data'] = alert_data['form_data']
#
#     return render(request, "catalog/contacts.html", context)



class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    template_name = 'catalog/product_add.html'
    fields = ['name', 'category', 'purchase_price', 'description', 'image',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all().order_by('name')
        return context

    def get_success_url(self):
        """Редирект на страницу созданного товара"""
        return reverse('catalog:product_details', args=[self.object.pk])

