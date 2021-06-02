from django.shortcuts import render
from django.views.generic import View
# Create your views here.
class BlogListView(View):
    def get(self, request):
        return render(request,'blog/blogs.html')

    def post(self, request, *args, **kwargs):
        pass