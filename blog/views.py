from blog.forms import CommentForm
from blog.models import Post, PostCategory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from django.contrib import messages


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
        print(self.object.id)
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()[:3]
        context["related_posts"] = self.object.tags.similar_objects()[:4]
        context["comment_form"] = CommentForm()
        comments = self.object.comment_post.all()
        comments_count = comments.count()
        context["comments"] = comments
        context["comments_count"] = comments_count
        categories = PostCategory.objects.all()
        context["categories"] = categories
        return context

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your Comment is submited successfully')
            return redirect('blog:blog-detail', slug=post.slug)



class SearchPostView(View):
    def get(self, request):
        q = request.GET.get('search-post')
        if q:
            queryset = Q(title__icontains=q)|Q(content__icontains=q)
            posts = Post.objects.filter(queryset).distinct()
        return render(request, 'blog/search_post.html', {'posts':posts, 'q':q})