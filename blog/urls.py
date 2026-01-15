from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path("blogpost_detail/<int:pk>/", BlogPostDetailView.as_view(), name="blogpost_detail"),
]