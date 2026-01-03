from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Product, Contact

# Create your views here.


def home(request):
    """Контроллер Главной страницы"""

    # Выборка последних 5 товаров по дате создания
    # order_by('-created_at') -> сортировка по убыванию даты (новые первыми)
    # [:5] → берём первые
    latest_products = Product.objects.order_by("-created_at")[:5]

    # Вывод в консоль
    print("Последние 5 товаров (вывод в консоль):")
    for i, product in enumerate(latest_products, 1):
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

    # Все контакты для отображения
    context = {'contacts': Contact.objects.all().order_by("-created_at")}

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        # Сохраняем данные для формы
        context['form_data'] = {'name': name, 'phone': phone, 'message': message}

        # Создаем и валидируем
        contact = Contact(name=name, phone=phone, message=message)

        try:
            contact.full_clean()
            contact.save()

            # Сохраняем в сессии для показа после редиректа
            request.session['contact_success'] = {
                'message': f"Спасибо, {name}! Ваше сообщение успешно отправлено."
            }

            # Редирект с сохранением успешного сообщения
            return redirect('/catalog/contacts/')

        except ValidationError as e:
            # Обрабатываем ошибку
            if 'phone' in e.message_dict:
                context['error'] = e.message_dict['phone'][0]
            elif 'name' in e.message_dict:
                context['error'] = e.message_dict['name'][0]
            else:
                context['error'] = "Ошибка при сохранении"

            # При ошибке показываем сразу (без редиректа)
            return render(request, "catalog/contacts.html", context)

    # GET запрос - проверяем успешные сообщения из сессии
    if 'contact_success' in request.session:
        success_data = request.session.pop('contact_success')
        context['success'] = True
        context['success_message'] = success_data['message']

    return render(request, "catalog/contacts.html", context)