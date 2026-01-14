from django.shortcuts import render
from .models import BlogPost
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

# Create your views here.

class BlogPostListView(ListView):
    template_name = 'blog/blog_list.html'
    model = BlogPost
