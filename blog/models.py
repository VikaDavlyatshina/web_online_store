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
        help_text="Когда было отправлено письмо о достижении 100 просмотров"
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

    # def save(self, *args, **kwargs):
    #     """Переопределяем save для отправки email при 100 просмотрах"""
    #
    #     # Условия:
    #     # 1. Просмотров больше 100
    #     # 2. Email еще не отправлялся (email_sent_at пустое)
    #     # 3. Это существующая запись (есть pk)
    #
    #     should_send_email = (
    #         self.views_count >= 100 and
    #         not self.email_sent_at
    #         and self.pk is not None
    #     )
    #
    #     super().save(*args, **kwargs)
    #
    #     if should_send_email:
    #         self.send_100_views_email()
    #         self.email_sent_at = timezone.now()
    #         BlogPost.objects.filter(pk=self.pk).update(email_sent_at=timezone.now())
    #
    # def send_100_views_email(self):
    #     """Функция для отправки письма при 100 просмотрах"""
    #
    #     subject = f"Ура! Статья {self.title} достигла 100 просмотров!"
    #     message = (f"Дорогой администратор! Позравляем, ваша статья {self.title} достигла 100 просмотр"
    #                f" Посмотреть статью: {self.get_absolute_url()}\n Поздравляем с популярностью")
    #
    #     send_mail(
    #         subject=subject,
    #         message=message,
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[settings.ADMIN_EMAIL],
    #         fail_silently=False,
    #     )


