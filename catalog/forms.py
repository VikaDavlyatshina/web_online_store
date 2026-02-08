from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product, Category, Contact


class StyleFormMixin:
    """
    Миксин для автоматической стилизации полей формы.
    Добавляет Bootstrap классы в зависимости от типа поля.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_bootstrap_classes()

    def _add_bootstrap_classes(self):
        """
        Добавляет Bootstrap CSS-классы ко всем полям формы.
        """
        for field in self.fields.values():
            widget = field.widget

            # Определяем нужный класс Bootstrap
            if isinstance(widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(widget, forms.Select):
                css_class = 'form-select'
            else:
                css_class = 'form-control'  # Для всех остальных

            # Добавляем класс
            if 'class' not in widget.attrs:
                widget.attrs['class'] = css_class

class ProductForm(StyleFormMixin, forms.ModelForm):
    """
    Форма создания и редактирования товара
    """

    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "owner"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Настраиваем поле image
        self._setup_image_field()

        # 2. Добавляем placeholder-ы
        self.fields["name"].widget.attrs["placeholder"] = 'Например: Набор для творчества'
        self.fields["purchase_price"].widget.attrs.update({
            "step": "0.1", "min": "1", "placeholder": "0.00"
        })
        self.fields["description"].widget.attrs.update({
            "rows": "4", "placeholder": "Опишите товар подробно..."
        })

        # 3. Настраиваем категорию
        self.fields["category"].empty_label = "Выберите категорию..."
        self.fields["category"].queryset = Category.objects.all().order_by("name")
        if not self.instance.pk:
            self.fields["category"].initial = None

    def _setup_image_field(self):
        """Настраиваем поле для загрузки изображения."""
        image_field = self.fields.get('image')
        if image_field and isinstance(image_field.widget, forms.ClearableFileInput):
            # Меняем английские тексты на русские
            image_field.widget.clear_checkbox_label = "Удалить изображение"
            image_field.widget.input_text = "Изменить изображение"
            image_field.widget.initial_text = "Текущее изображение"

            # Добавляем accept для изображений
            image_field.widget.attrs['accept'] = 'image/*'

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
                raise ValidationError(f"Название содержит запрещенное слово: {forbidden_word}")

        return name

    def clean_description(self):
        """Проверка, содержит ли Описание запрещенные слова"""
        description = self.cleaned_data.get("description", "")

        # Проверяем только если описание не пустое
        if description:
            description_lower = description.lower()
            for forbidden_word in self.FORBIDDEN_WORDS:
                if forbidden_word in description_lower:
                    raise ValidationError(f"Описание содержит запрещенное слово: {forbidden_word}")

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


class ContactForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для контактов.
    """

    class Meta:
        model = Contact
        exclude = [
            "created_at",
        ]
        error_messages = {
            "name": {"required": "Пожалуйста, введите ваше имя"},
            "message": {"required": "Пожалуйста, введите сообщение"},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Добавляем Placeholders
        self.fields["name"].widget.attrs["placeholder"] = "Ваше имя"
        self.fields["email"].widget.attrs["placeholder"] = "ваш@email.com"
        self.fields["phone"].widget.attrs["placeholder"] = "+7 (999) 123-45-67"
        self.fields["message"].widget.attrs["placeholder"] = "Ваше сообщение..."
        self.fields["message"].widget.attrs["rows"] = 4

    def clean(self):
        """Проверка: email или телефон обязательно"""
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        # Безопасная проверка email
        email_str = ""
        if email is not None:
            email_str = str(email).strip()

        # Проверка, что есть или телефон, или email
        if not email_str and not phone:
            raise ValidationError("Укажите email или телефон для связи")

        return cleaned_data

    def clean_name(self):
        """Проверка имени"""
        name = self.cleaned_data.get("name")

        if name is None:
            raise ValidationError("Пожалуйста, введите ваше имя")

        name = name.strip()

        if len(name) < 2:
            raise ValidationError("Имя должно быть не короче двух букв")

        if not name.replace(" ", "").replace("-", "").isalpha():
            raise ValidationError("Имя должно содержать только буквы")

        return name

    def clean_email(self):
        """Проверка email (если указан)"""
        email = self.cleaned_data.get("email")

        if email is not None:
            email = str(email).strip()

            if email:  # если не пустая строка
                if "@" not in email:
                    raise ValidationError("Email должен содержать символ @")
                if "." not in email.split("@")[-1]:
                    raise ValidationError("Email должен содержать домен")

        return email

    def clean_phone(self):
        """Проверка телефона (если указан)"""
        phone = self.cleaned_data.get("phone")

        if phone:
            phone_str = str(phone)
            if not phone_str.startswith("+7"):
                raise ValidationError("Введите российский номер телефона (+7)")

        return phone

    def clean_message(self):
        """Проверка сообщения"""
        message = self.cleaned_data.get("message")

        if message is None:
            raise ValidationError("Пожалуйста, введите сообщение")

        message = message.strip()

        if len(message) < 10:
            raise ValidationError("Сообщение должно быть не короче 10 символов")

        forbidden_words = ["казино", "криптовалюта", "биржа", "спам"]
        message_lower = message.lower()

        for word in forbidden_words:
            if word in message_lower:
                raise ValidationError(f'Сообщение содержит запрещенное слово: "{word}"')

        return message
