from decimal import Decimal
from delivery.models import DeliveryType
from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import OrderCreationForm
from cart.cart import Cart
from .models import OrderItem
from django.urls import reverse
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
            if cart.delivery:
                delivery = DeliveryType.objects.get(location=cart.delivery, type_of_delivery=cart.get_delivery_status())
                order.delivery = delivery
                order.delivery_charge = cart.get_delivery_charge()
            order.save()
            if request.user.is_authenticated:
                order.user = request.user
                print("order user:", order.user)
                order.save()
            for item in cart:
                
                order_item = OrderItem.objects.create(
                    order=order, products=item['product'], price=item['price'], quantity=item['quantity'])
                order_item.products.stock -= item['quantity']
                order_item.products.save()
                order_item.save()
            #clear cart
            cart.clear()
            return redirect(reverse('payment:pay-payment', kwargs={'pk': order.pk}))
