from decimal import Decimal
from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import OrderCreationForm
from cart.cart import Cart
from .models import OrderItem
from decimal import Decimal
# Create your views here.


class OrderCreateView(View):
    def get(self, request, *args, **kwargs):
        form = OrderCreationForm()
        cart = Cart(request)
        return render(request, 'order/create.html', {'form': form, 'cart': cart})

    def post(self, request, *args, **kwargs):
        form = OrderCreationForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount_percentage
            order.save()
            if request.user.is_authenticated:
                order.user = request.user
                print("order user:", order.user)
                order.save()
            for item in cart:
                a=item['price']
                print(type(a))
                OrderItem.objects.create(
                    order=order, products=item['product'], price=item['price'], quantity=item['quantity'])
            #clear cart
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
