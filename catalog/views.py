from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Product, Contact, Category
from django.views.generic import ListView, DetailView

# Create your views here.


class ProductListView(ListView):
    model = Product

    ordering = ["-created_at"]
    paginate_by = 6



# def home(request):
#     """Контроллер Главной страницы"""
#
#     # order_by('-created_at') -> сортировка по убыванию даты (новые первыми)
#
#     all_products = Product.objects.order_by("-created_at")
#
#     # Вывод в консоль
#     print("Последние 5 товаров (вывод в консоль):")
#     for i, product in enumerate(all_products[:5], 1):
#         print(
#             f"{i}. {product.name}\n"
#             f"Цена: {product.purchase_price}\n"
#             f"Категория: {product.category.name if product.category else 'Без категории'}\n"
#             f"Создан: {product.created_at}\n"
#         )
#
#     # Создаем пагинатор: 6 товаров на страницу
#     paginator = Paginator(all_products, 6)
#
#     # Получаем номер страницы из GET-параметра
#     page_number = request.GET.get('page')
#
#     # Получаем объект страницы
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'page_obj': page_obj,
#          'paginator': paginator
#     }
#
#
#     return render(request, "catalog/product_list.html", context)


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

class ProductDetailView(DetailView):
    model = Product


# def product_details(request, pk):
#     """Контроллер страницы Товара"""
#     product = Product.objects.get(pk=pk)
#
#     # Базовый контекст
#     context = {
#         'product': product
#     }
#     return render(request, "catalog/product_detail.html", context)

def product_add(request):
    """Контроллер страницы Добавления товар"""

    # Базовый контекст - все категории
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories
    }

    # Обработка POST-запроса (отправка формы)
    if request.method == "POST":
        # Получаем данные из формы
        form_data = {
            'name': request.POST.get("name", "").strip(),  # было name, стало title
            'category_id': request.POST.get("category", "").strip(),  # получаем ID категории
            'price': request.POST.get("price", "").strip(),
            'description': request.POST.get("description", "").strip(),
        }

        #  Получаем файл изображения
        image = request.FILES.get("image")

        # Преобразуем цену в число
        try:
            form_data['price'] = float(form_data['price'])
        except (ValueError, TypeError):
            raise ValidationError({'price': 'Цена должна быть числом'})

        # Находим категорию по ID
        category_id = form_data.pop('category_id')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError({'category': 'Категория не найдена'})
        except ValueError:
            raise ValidationError({'category': 'Некорректный ID категории'})

        # Создаем товар
        product = Product(
            name=form_data['name'],
            category=category,
            purchase_price=form_data['price'],
            description=form_data['description'],
        )

        # Если есть фото - сохраняем
        if image:
            product.image = image

        # Валидируем и сохраняем
        product.full_clean()
        product.save()

        return redirect(reverse('catalog:product_details', args=[product.pk]))



    return render(request, "catalog/product_add.html", context)