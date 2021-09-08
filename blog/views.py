from blog.models import Post
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.db.models import Q


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



class SearchPostView(View):
    def get(self, request):
        q = request.GET.get('search-post')
        if q:
            queryset = Q(title__icontains=q)|Q(content__icontains=q)
            posts = Post.objects.filter(queryset).distinct()
        return render(request, 'blog/search_post.html', {'posts':posts, 'q':q})