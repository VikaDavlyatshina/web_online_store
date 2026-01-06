from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Product, Contact

# Create your views here.


def home(request):
    """Контроллер Главной страницы"""

    # Выборка последних 5 товаров по дате создания
    # order_by('-created_at') -> сортировка по убыванию даты (новые первыми)
    # [:5] → берём первые
    latest_products = Product.objects.order_by("-created_at")

    # Вывод в консоль
    print("Последние 5 товаров (вывод в консоль):")
    for i, product in enumerate(latest_products[:5], 1):
        print(
            f"{i}. {product.name}\n"
            f"Цена: {product.purchase_price}\n"
            f"Категория: {product.category.name if product.category else 'Без категории'}\n"
            f"Создан: {product.created_at}\n"
        )

    # Передаём в шаблон
    context = {"title": "Главная страница", "latest_products": latest_products}

    return render(request, "catalog/home.html", context)


def contacts(request):
    """Контроллер страницы Контактов"""

    # Базовый контекст
    context = {
        'contacts': Contact.objects.all().order_by("-created_at")
    }

    # Обработка POST-запроса (отправка формы)
    if request.method == "POST":
        # Получаем данные из формы
        form_data = {
            'name': request.POST.get("name", "").strip(),
            'phone': request.POST.get("phone", "").strip(),
            'message': request.POST.get("message", "").strip()
        }

        try:
            # Создаем и валидируем контакт
            contact = Contact(**form_data)
            contact.full_clean()
            contact.save()

            # Успешное сообщение
            request.session['contact_alert'] = {
                'type': 'success',
                'message': f"Спасибо, {contact.name}! Сообщение отправлено.",
            }

        except ValidationError as e:
            # Формируем сообщения об ошибках
            errors = []
            field_names = {'name': 'Имя', 'phone': 'Телефон', 'message': 'Сообщение'}

            for field, name in field_names.items():
                if field in e.message_dict:
                    errors.append(f"{name}: {e.message_dict[field][0]}")

            if not errors and e.messages:
                errors = list(e.messages)

            # Формируем итоговое сообщение
            if errors:
                error_text = f"Пожалуйста исправьте ошибки перед отправкой: {'; '.join(errors)}"
            else:
                error_text = "Произошла ошибка при отправке сообщения"

            # Сообщение об ошибке
            request.session['contact_alert'] = {
                'type': 'error',
                'message': error_text,
                'form_data': form_data
            }

        # Редирект после POST
        return redirect(reverse('catalog:contacts'))

    # Обработка GET-запроса (отображение страницы)

    # Проверяем сообщения из сессии
    if 'contact_alert' in request.session:
        alert_data = request.session.pop('contact_alert')

        context['alert'] = {
            'type': alert_data['type'],
            'message': alert_data['message']
        }

        # Восстанавливаем данные формы
        if 'form_data' in alert_data:
            context['form_data'] = alert_data['form_data']

    return render(request, "catalog/contacts.html", context)

def product_details(request, pk):
    """Контроллер страницы Товара"""
    product = Product.objects.get(pk=pk)

    # Базовый контекст
    context = {
        'product': product
    }
    return render(request, "catalog/product_details.html", context)