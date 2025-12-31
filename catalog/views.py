from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    context = {}  # Создаём пустой контекст

    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        # Для отладки
        print(f"Сообщение от {name}: {message[:50]}")

        # Добавляем сообщение об успехе в контекст
        context['success'] = True
        context['success_message'] = f'Спасибо, {name}! Ваше сообщение успешно отправлено.'

    return render(request, 'catalog/contacts.html', context)