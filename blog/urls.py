from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path("blogpost_detail/<int:pk>/", BlogPostDetailView.as_view(), name="blogpost_detail"),
    path('blogpost_create/', BlogPostCreateView.as_view(), name="blogpost_create"),
    path('<int:pk>/blogpost_update/', BlogPostUpdateView.as_view(), name="blogpost_update"),
    path('<int:pk>/blogpost_delete/', BlogPostDeleteView.as_view(), name="blogpost_delete"),
]