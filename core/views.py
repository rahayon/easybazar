from product.models import Category, Product
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        latest_categories = categories.order_by('-id')[:8]
        products = Product.objects.all()
        featured_categories = categories.filter(product__is_featured=True)[:5]
        featured_product = products.filter(is_featured=True)[:20]
        latest_products = Category.latest_product(self.request).prefetch_related('product')
        top_rated_products = Product.get_average_rating_product(self.request)
        context = {
            'latest_categories': latest_categories,
            'products': products,
            'featured_categories':featured_categories,
            'featured_products':featured_product,
            'latest_products': latest_products,
            'top_rated_products': top_rated_products
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