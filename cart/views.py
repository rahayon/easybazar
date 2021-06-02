from coupon.forms import CouponApplyForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from product.models import Product

# Create your views here.


class CartAdd(View):
    def post(self, request, product_id, *args, **kwargs):
        form = CartAddProductForm(request.POST)
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            update_quantity = form.cleaned_data['update_quantity']
            product_id = str(product.id)
            cart.add(product=product, quantity=quantity,
                     update_quantity=update_quantity)
            return redirect("cart:cart-detail")


class CartRemove(View):
    def post(self, request, product_id, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart-detail')




class CartDetail(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'], 'update_quantity': True})
        coupon_apply_form = CouponApplyForm()
        return render(request, 'cart/cart_detail.html', {'cart': cart, 'coupon_apply_form':coupon_apply_form})
