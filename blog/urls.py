from django.urls import path
from blog.views import BlogDetailView, BlogListView, SearchPostView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('post/<slug:slug>/',BlogDetailView.as_view(), name='blog-detail'),
    path('search_post/', SearchPostView.as_view(), name='search-posts'),
]
