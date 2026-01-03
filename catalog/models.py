from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator

# Create your models here.


def get_default_category_id():
    """Возвращает ID категории 'Без категории' или создает ее"""
    # чтобы избежать циклического импорта
    from django.apps import apps

    category_model = apps.get_model("catalog", "Category")
    category, created = category_model.objects.get_or_create(
        name="Без категории",
        defaults={"descriptions": "Товары без указанной категории"},
    )
    return category.id


class Category(models.Model):
    """ Модель для Категории"""
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование категории",
        help_text="Введите название категории",
        unique=True,  # Названия Категории должны быть уникальными
    )
    descriptions = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        blank=True,
        null=True,
        max_length=2000,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Модель для Продукта(Товара)"""
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование товара",
        help_text="Введите название товара",
        db_index=True,  # Создает индекс в БД для быстрого поиска и сортировки
    )
    descriptions = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание товара",
        blank=True,
        null=True,
        max_length=2000,
    )
    image = models.ImageField(
        upload_to="catalog/product_photo",
        blank=settings.DEBUG,  # Разрешаем пустое ТОЛЬКО в режиме отладки (DEBUG=True)
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото товара",
    )  #
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,  # При удалении категории, у товара category станет DEFAULT
        default=get_default_category_id,  # Используем функцию
        verbose_name="Категория",
        help_text="Введите категорию товара",
        related_name="products",  # Позволяет получать все товары категории: category.products.all()
    )
    purchase_price = models.DecimalField(
        max_digits=10,  # До 10 млн рублей
        decimal_places=2,  # 2 знака = копейки
        validators=[
            MinValueValidator(
                1,  # Минимальная цена - 1 рубль
                message="Цена должна быть больше нуля. Минимум 1 рубль",
            )
        ],
        verbose_name="Цена за покупку (руб.)",
        help_text="Укажите цену в рублях с копейками. Минимальная цена: 1 рубль",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"  # Автоматически при создании
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # Автоматически при сохранении
        verbose_name="Дата последнего изменения",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} - {self.purchase_price} руб."


class Contact(models.Model):
    """ Модель для Контактов"""
    name = models.CharField(
        max_length=150,
        verbose_name="Имя пользователя",
        help_text="Введите ваше имя",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        help_text="Введите контактный телефон",
        validators= [
            RegexValidator(
                regex=r'^(?=(?:\D*\d){5,})[\d\s\-\+\(\)]+$',
                message='Номер должен содержать минимум 5 цифр и только цифры, пробелы, +, -, (, )'
            )]
    )
    message = models.TextField(
        verbose_name="Сообщение",
        help_text="Введите ваше сообщение",
        max_length=2000,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["-created_at"]
        indexes = [
        models.Index(fields=['-created_at']),
        models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.phone}) - {self.created_at.strftime('%d.%m.%Y %H:%M')}"