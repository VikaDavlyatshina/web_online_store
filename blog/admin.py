from django.contrib import admin

from blog.models import BlogPost


# Register your models here.


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','is_published', 'created_at', 'views_count')  # Поля для отображения в админке
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'created_at', 'content')
    list_editable = ('is_published',)  # Можно менять статус прямо в списке