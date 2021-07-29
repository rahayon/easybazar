from delivery.forms import DeliveryForm
from product.models import Category, Product
from  delivery.models import DeliveryLocation, DeliveryType
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.http import HttpResponseRedirect
from blog.models import Post

# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        latest_categories = categories.order_by('-id')[:8]
        products = Product.objects.all()
        featured_categories = categories.filter(product__is_featured=True)[:5]
        featured_product = products.filter(is_featured=True)[:20]
        latest_products = products.order_by('-id')[:9]
        top_rated_products = Product.get_average_rating_product(self.request)
        recent_posts = Post.objects.all()[:3]
        
        context = {
            'latest_categories': latest_categories,
            'products': products,
            'featured_categories':featured_categories,
            'featured_products':featured_product,
            'latest_products': latest_products,
            'top_rated_products': top_rated_products,
            'recent_posts': recent_posts
        }
        return render(request, 'core/index.html',context)

    # def post(self, request, *args, **kwargs):
    #     delivery_form = DeliveryForm(request.POST)
    #     if delivery_form.is_valid():
    #         delivery_location = delivery_form.cleaned_data['delivery']
    #         context = {
    #             'location':delivery_location,
    #             'delivery_location': delivery_form,
    #         }
    #         return render(request, 'core/index.html',context)

class ContactUsView(View):
    """ যোগাযোগ করার জন্য """
    def get(self, request):
        return render(request,'core/contact_us.html')

    def post(self, request):
        pass

class FreeShipping(View):
    def post(self, request):
        delivery_form = DeliveryForm(request.POST)
        if delivery_form.is_valid():
            delivery_location = delivery_form.cleaned_data['delivery']
            context = {
                'location':delivery_location,
                'delivery_location': delivery_form,
            }
            return render(request, 'core/index.html',context)