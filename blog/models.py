from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.


class BlogPost(models.Model):
    """
    Модель Блоговой записи
    Поля:
    1. заголовок
    2. содержимое
    3. превью (изображение)
    4. дата создания
    5. признак публикации (булевое поле)
    6. количество просмотров
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Заголовок статьи - не более 200 символов",
    )

    content = models.TextField(verbose_name="Содержимое статьи")

    preview = models.ImageField(
        upload_to="blog/preview",
        verbose_name="Превью",
        help_text="Загрузите фото для блога",
        blank=settings.DEBUG,  # Разрешаем пустое ТОЛЬКО в режиме отладки (DEBUG=True)
        null=True,  # Может быть NULL в БД
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Автоматически при создании
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")  # По умолчанию не опубликовано

    views_count = models.PositiveIntegerField(
        verbose_name="Количество просмотров",
        help_text="Укажите количество просмотров",
        default=0,  # Поле для хранения просмотров
    )

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Получение абсолютной ссылки для Поста блога"""
        return reverse("blog:blogpost_detail", kwargs={"pk": self.pk})
