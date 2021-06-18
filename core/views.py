from product.models import Category, Product
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('-id')[:8]
        products = Product.objects.all()
        context = {
            'latest_categories': categories,
            'products': products
        }
        return render(request, 'core/index.html',context)

    def post(self, request, *args, **kwargs):
        pass

class ContactUsView(View):
    """ যোগাযোগ করার জন্য """
    def get(self, request):
        return render(request,'core/contact_us.html')

    def post(self, request):
        pass