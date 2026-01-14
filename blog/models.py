from django.db import models
from django.urls import reverse

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
        help_text="Заголовок статьи - не более 200 символов")

    content = models.TextField(
        verbose_name="Содержимое статьи")

    preview= models.ImageField(
        upload_to="blog/preview",
        verbose_name="Превью",
        blank=True,   # Можно оставить пустым в форме
        null=True     # Может быть NULL в БД
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"  # Автоматически при создании
    )
    is_published= models.BooleanField(
        default=False,    # По умолчанию не опубликовано
        verbose_name="Опубликовано"
    )

    views_count = models.PositiveIntegerField(
        default=0,   # Поле для хранения просмотров
        verbose_name="Количество публикаций"
    )

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"
        ordering = ['-created_at']

        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse('blogpost_detail', kwargs={'pk': self.pk})
