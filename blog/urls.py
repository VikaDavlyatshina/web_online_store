from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogPostListView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
]