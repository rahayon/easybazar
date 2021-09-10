from core.forms import ContactForm
from delivery.forms import DeliveryForm
from product.models import Category, Product
from delivery.models import DeliveryLocation, DeliveryType
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.http import HttpResponseRedirect
from blog.models import Post
from django.contrib import messages
from .models import Banner

# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        latest_categories = categories.order_by('-id')[:8]
        products = Product.objects.all()
        featured_categories = categories.filter(product__is_featured=True)[:5]
        featured_product = products.filter(is_featured=True)[:20]
        latest_products = products.order_by('-id')[:6]
        top_rated_products = Product.get_average_rating_product(self.request)
        recent_posts = Post.objects.all()[:3]
        best_selling_products = products.order_by('on_sale')[:6]
        hero_banner = Banner.objects.first()
        latest_offer = products.filter(is_offer=True).order_by('-created_at')[:2]
        
        context = {
            'latest_categories': latest_categories,
            'products': products,
            'featured_categories':featured_categories,
            'featured_products':featured_product,
            'latest_products': latest_products,
            'top_rated_products': top_rated_products,
            'recent_posts': recent_posts,
            'best_selling_products':best_selling_products,
            'hero_banner': hero_banner,
            'latest_offer':latest_offer
        }
        return render(request, 'core/index.html',context)



class ContactUsView(View):
    """ যোগাযোগ করার জন্য """
    def get(self, request):
        form = ContactForm()
        return render(request,'core/contact_us.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Messages has sent successfully.")
        return redirect('core:contact-us')

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