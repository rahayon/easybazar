from blog.models import Post
from django.shortcuts import render
from django.views.generic import ListView, DetailView


# Create your views here.
class BlogListView(ListView):
    model = Post
    template_name = 'blog/blogs.html'
    context_object_name = 'posts'
    paginate_by = 8
    ordering = '-created_at'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()[:3]
        return context
