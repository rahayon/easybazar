from typing import get_args
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from math import ceil
# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_product"] = Product.objects.all()[:6]
        context["categories"] = Category.latest_product(self.request).prefetch_related('product')
        context["discount_products"] = Product.discount_product(self.request)
        return context

class ProductDetail(DetailView):
    model = Product
    template_name='product/product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartAddProductForm()
        return context

    


    
    

    
    
    
    