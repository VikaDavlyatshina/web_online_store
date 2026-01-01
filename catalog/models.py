from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование категории",
        help_text="Введите название категории",
    )
    descriptions = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование товара",
        help_text="Введите название товара",
    )
    descriptions = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание товара",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="catalog/product_photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото товара",
    )  #
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию товара",
        blank=True,
        null=True,
        related_name="products",
    )
    purchase_price = models.DecimalField(
        max_digits=10,  # До 10 млн рублей
        decimal_places=2,  # 2 знака = копейки
        validators=[MinValueValidator(0)],  # Цена не может быть отрицательной
        verbose_name="Цена за покупку (руб.)",
        help_text="Укажите цену в рублях с копейками",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # Автоматически при создании
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # Автоматически при сохранении
        verbose_name="Дата последнего изменения"
    )
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} - {self.purchase_price} руб."
