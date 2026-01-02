from django.shortcuts import render
from .models import Product

# Create your views here.


def home(request):
    """ Контроллер Главной страницы """

    # Выборка последних 5 товаров по дате создания
    # order_by('-created_at') -> сортировка по убыванию даты (новые первыми)
    # [:5] → берём первые
    latest_products = Product.objects.order_by('-created_at')[:5]


    # Вывод в консоль
    print("Последние 5 товаров (вывод в консоль):")
    for i, product in enumerate(latest_products, 1):
        print(f"{i}. {product.name}\n"
              f"Цена: {product.purchase_price}\n"
              f"Категория: {product.category.name if product.category else 'Без категории'}\n"
              f"Создан: {product.created_at}\n")

    # Передаём в шаблон
    context = {
        'title': 'Главная страница',
        'latest_product': latest_products
    }

    return render(request, "catalog/home.html", context)


def contacts(request):
    context = {}  # Создаём пустой контекст

    if request.method == "POST":
        # Получаем данные из формы
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        message = request.POST.get("message", "")

        # Для отладки
        print(f"Сообщение от {name}: {message[:50]}")

        # Добавляем сообщение об успехе в контекст
        context["success"] = True
        context["success_message"] = (
            f"Спасибо, {name}! Ваше сообщение успешно отправлено."
        )

    return render(request, "catalog/contacts.html", context)
