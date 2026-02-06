from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product, Category



class StyleFormMixin:
    """
    Миксин для автоматической стилизации полей формы.
    Добавляет Bootstrap классы в зависимости от типа поля.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Проходим по всем полям формы
        for field_name, field, in self.fields.items():
            # Проверяем тип виджета
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(widget, forms.SelectMultiple):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(widget, forms.RadioSelect):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                # Для TextInput, NumberInput, EmailInput, Textarea, FileInput и т.д.
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ["name", "category", "purchase_price", "description", "image", "is_published"]



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Placeholders и специфические атрибуты
        self.fields['name'].widget.attrs['placeholder'] = 'Например: Набор для творчества "Алмазная мозаика"'

        self.fields['purchase_price'].widget.attrs.update({
            'step': '0.1',
            'min': '1',
            'placeholder': '0.00'
        })

        self.fields['description'].widget.attrs.update({
            'rows': '4',
            'placeholder': 'Опишите товар подробно: материалы, размеры, особенности...'
        })

        # Настройка Категории
        self.fields['category'].empty_label = "Выберите категорию..."
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        if not self.instance.pk:
            self.fields['category'].initial = None


        # Убираем стандартные подписи Django для изображения
        self.fields['image'].widget.clear_checkbox_label = "Очистить"
        self.fields['image'].widget.input_text = "Изменить"
        self.fields['image'].widget.initial_text = "Текущее"


    def clean_name(self):
        """Проверка, содержит ли Название запрещенные слова"""
        name = self.cleaned_data.get("name", "")

        if not name:
            raise ValidationError("Название товара обязательно")

        if len(name) < 5:
            raise ValidationError("Название должно содержать минимум 5 символов")

            # Проверка, что есть буквы (не только цифры и символы)
        if not any(char.isalpha() for char in name):
            raise ValidationError("Название должно содержать буквы")

        name_lower = name.lower()
        for forbidden_word in self.FORBIDDEN_WORDS:
            if forbidden_word in name_lower:
                raise ValidationError(
                    f"Название содержит запрещенное слово: {forbidden_word}"
                )

        return name

    def clean_description(self):
        """Проверка, содержит ли Описание запрещенные слова"""
        description = self.cleaned_data.get("description", "")

        # Проверяем только если описание не пустое
        if description:
            description_lower = description.lower()
            for forbidden_word in self.FORBIDDEN_WORDS:
                if forbidden_word in description_lower:
                    raise ValidationError(
                        f"Описание содержит запрещенное слово: {forbidden_word}"
                    )

        return description

    def clean_purchase_price(self):
        """Проверка цены"""
        purchase_price = self.cleaned_data.get("purchase_price")

        if purchase_price is not None and purchase_price <= 0:
            raise ValidationError("Цена не может быть отрицательной!")

        return purchase_price

    def clean_image(self):
        """Проверка изображения"""
        image = self.cleaned_data.get("image")

        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Фото слишком большое! Максимум 5 MB.")

        return image
