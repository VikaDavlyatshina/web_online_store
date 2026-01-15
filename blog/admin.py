from django.contrib import admin

from blog.models import BlogPost


# Register your models here.


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления записями блога.

    Особенности:
    - Показывает кнопку для просмотра статьи на сайте
    - Позволяет быстро фильтровать и искать статьи
    - Редактирование статуса публикации прямо в списке
    """

    # Какие поля показывать в списке
    list_display = ('title',
                    'view_on_site_link',
                    'is_published',
                    'views_count'
                    'created_at',
                    )
    # Фильтры справа
    list_filter = ('is_published', 'created_at')

    # Поиск по этим полям
    search_fields = ('title', 'content')

    # Редактируемые прямо в списке
    list_editable = ('is_published',)

    # Порядок сортировки по умолчанию
    ordering = ('-created_at',)

