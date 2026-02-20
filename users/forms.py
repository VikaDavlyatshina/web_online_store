from django import forms
from django.contrib.auth.forms import UserCreationForm

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем placeholder для email
        self.fields["email"].widget.attrs["placeholder"] = "ваш@email.com"


class UserProfileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["phone", "country", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Настраиваем поле avatar
        self._setup_avatar_field()

        # 2. Добавляем placeholder-ы
        self.fields["phone"].widget.attrs["placeholder"] = "+7 (999) 123-45-67"
        self.fields["country"].widget.attrs["placeholder"] = "Россия"

        # 3. Делаем поля необязательными
        self.fields["phone"].required = False
        self.fields["country"].required = False
        self.fields["avatar"].required = False

    def _setup_avatar_field(self):
        """Настраиваем поле для загрузки аватара."""
        avatar_field = self.fields.get('avatar')
        if avatar_field and isinstance(avatar_field.widget, forms.ClearableFileInput):
            avatar_field.widget.clear_checkbox_label = "Удалить аватар"
            avatar_field.widget.input_text = "Изменить аватар"
            avatar_field.widget.initial_text = "Текущий аватар"
            avatar_field.widget.attrs['accept'] = 'image/*'
