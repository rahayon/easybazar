from django.http import request
from order.models import Order, OrderItem
from django.contrib import messages
from product.forms import ReviewForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from .models import Category, Product, ReviewRating
from cart.forms import CartAddProductForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from math import ceil
from django.db.models import Q


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 6

    # ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_products"] = Product.objects.all().order_by('-id')[:9]
        context["discount_products"] = Product.discount_product(self.request)
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartAddProductForm()
        context['related_products'] = self.object.tags.similar_objects()[:4]
        if self.request.user.is_authenticated:
            context['orderproduct'] = OrderItem.objects.filter(order__user=self.request.user,
                                                               products=self.object).exists()
        else:
            context['orderproduct'] = None
        context['reviews'] = ReviewRating.objects.filter(product=self.object, status=True)
        return context


class OurOffersView(View):
    def get(self, request):
        products = Product.objects.filter(is_offer=True)
        return render(request, 'product/product_offers.html', {'products':products})

class OfferDetailView(View):
    pass
class SearchProductView(View):
    def get(self, request):
        q = request.GET.get('search-product')
        if q:
            queryset = Q(name__icontains=q)
            products = Product.objects.filter(queryset).distinct()
        return render(request, 'product/search_product.html', {'products':products, 'q':q})
class CategoryDetail(DetailView):
    model = Category
    template_name = 'product/category_detail.html'
    context_object_name = 'category'




class SubmitReview(View):
    def post(self, request, product_id):
        rating = request.POST.get('rating')
        subject = request.POST.get('subject')
        review = request.POST.get('review')
        product = get_object_or_404(Product, id=product_id)

        try:
            reviews = ReviewRating.objects.get(user=request.user, product=product)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect(reverse('product:Product_detail', kwargs={'slug': product.slug}))
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                print("form valid")
                data = ReviewRating()
                data.user = request.user
                data.product = product
                data.rating = rating
                data.subject = subject
                data.review = review
                data.save()
                messages.success(request, 'Your review has been submited!')
                return redirect(reverse('product:Product_detail', kwargs={'slug': product.slug}))


# class ProdouctFilterView(View):
#     def get(self, request):
#         products = ProductFilter(request.GET, queryset=Product.objects.all())
#         return render(request, 'product/product_filter.html', {'products': products})