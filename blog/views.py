from django.urls import reverse_lazy, reverse

from .models import BlogPost
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView


# Create your views here.

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'   # Контекстное имя, чтобы использовать в шаблонах

    def get_queryset(self):
        """
        Переопределение метода.
        Выводятся только опубликованные статьи
        """

        return super().get_queryset().filter(is_published=True)

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'  # Контекстное имя, чтобы использовать в шаблонах

    def get_object(self, queryset=None):
        """
        Переопределение метода для подсчета просмотров статьи.
        При открытии статьи увеличиваем счетчик просмотров
        """

        # Получаем статью из базы данных
        post = super().get_object(queryset)

        # Увеличиваем счетчик просмотров
        post.views_count += 1
        post.save(update_fields=['views_count'])

        # Сохраняем для использования в других методах
        self.object = post

        return post

class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blog:blog_list')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ('title', 'content', 'preview', 'is_published')

    def get_success_url(self):
        return reverse_lazy('blog:blogpost_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:blog_list')
