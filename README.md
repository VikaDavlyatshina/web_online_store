# Проект web_online_store
Учебный проект интернет-магазина.

## Описание:
Проект интернет-магазин, разработанный в рамках курса по Django. Проект будет постепенно дорабатываться от базовой
структуры до полноценного e-commerce решения.

**Основные цели**
- Практическое освоение Django и сопутствующих технологий
- Создание портфолио проекта
- Поэтапное развитие от простого к сложному

## Технологии
- **Backend**: Django 6.0
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Package manager**: Poetry
- **Version control**: Git + GitFlow
- **Python**: 3.13+

## Структура проекта

```plaintext
web-online-store/
│
├── config/            #  Конфигурация проекта
│   ├── settings/      #  Настройки по средам
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py        #  Главные URL
│   └── wsgi.py
│
├── catalog/               #  Приложение каталога
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore               #   Игнорируемые файлы
├── manage.py                #   Django CLI
├── pyproject.toml          #   Зависимости Poetry
├── poetry.lock            #   Фиксированные версии
└── README.md              #   Документация
```

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/VikaDavlyatshina/web_online_store.git
   cd web_online_store
   
2. Установите зависимости с помощью Poetry:
   ```bash
   poetry install
   
3. Запустите миграции: 
   ```bash
     python manage.py migrate
   
4. Запустите сервер: 
   ```bash
   python manage.py runserver

## GitFlow
Проект использует GitFlow для организации разработки:

```text
main        - стабильная версия (релизы)
develop     - текущая разработка
feature/*   - ветки для новых функций
```

```
# Создание ветки для задания
git checkout develop
git checkout -b feature/homework-3

# После выполнения
git add .
git commit -m "Homework 3: Create HTML templates with Bootstrap"
git push origin feature/homework-3

# Создать Pull Request для слияния в develop
```
