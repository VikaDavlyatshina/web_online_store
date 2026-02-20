from django.utils import timezone

from django.core.mail import send_mail
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

    email_sent_at = models.DateTimeField(
        verbose_name="Дата отправки email о 100 просмотрах",
        null=True,
        blank=True,
        help_text="Когда было отправлено письмо о достижении 100 просмотров",
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

    def save(self, *args, **kwargs):
        """Переопределяем save для отправки email при 100 просмотрах"""

        # Запоминаем старые значения ДО сохранения
        if self.pk:  # Если запись уже существует
            try:
                old_instance = BlogPost.objects.get(pk=self.pk)
                old_views = old_instance.views_count
                old_email_sent = old_instance.email_sent_at
            except BlogPost.DoesNotExist:
                old_views = 0
                old_email_sent = None
        else:  # Если это новая запись
            old_views = 0
            old_email_sent = None

        # Сначала сохраняем запись
        super().save(*args, **kwargs)

        # Проверяем условия ПОСЛЕ сохранения
        has_100_views = self.views_count >= 100
        email_not_sent = not old_email_sent
        just_passed_100 = old_views < 100
        is_existing = self.pk is not None

        should_send_email = has_100_views and email_not_sent and just_passed_100 and is_existing
        if should_send_email:
            # Отправляем письмо
            self.send_100_views_email()

            # Обновляем поле с датой отправки
            self.email_sent_at = timezone.now()

            # Сохраняем ТОЛЬКО поле email_sent_at (чтобы не создавать рекурсию)
            super().save(update_fields=['email_sent_at'])

    def send_100_views_email(self):
        """Функция для отправки письма при 100 просмотрах"""

        subject = f"Ура! Статья '{self.title}' достигла 100 просмотров!"

        # Для разработки используйте localhost
        domain = "127.0.0.1:8000"

        # Полный URL статьи
        full_url = f"http://{domain}{self.get_absolute_url()}"

        html_message = f"""
        <html>
            <body>
                <h2>Дорогой администратор!</h2>
                <p>Поздравляем! Ваша статья <strong>"{self.title}"</strong> достигла 100 просмотров!</p>
                <p><a href="{full_url}">Посмотреть статью</a></p>
            </body>
        </html>
        """

        send_mail(
            subject=subject,
            message=f"Посмотреть статью: {full_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )