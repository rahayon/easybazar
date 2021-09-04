from decimal import Decimal
from delivery.models import DeliveryType
from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import OrderCreationForm
from cart.cart import Cart
from .models import Order, OrderItem
from django.urls import reverse
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


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
            create_account = request.POST.get('create_account')
            password = request.POST.get('password')
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
            if create_account:
                if CustomUser.objects.filter(mobile=order.mobile_number).exists():
                    messages.error(
                        request, "Customer with this  {0} number is already exists".format(order.mobile_number))
                else:
                    password_hash = make_password(password)
                    user = CustomUser.objects.create(mobile=order.mobile_number, password=password_hash)

                    if order.email:
                        user.email = order.email
                        user.save()

                    user.profile.full_name = order.full_name
                    user.profile.address = order.address
                    user.profile.save()
                    user.save()
                    order.user = user
                    order.save()

                    login(request, user)
                    messages.success(
                        request, "Account for {0} is created Successfully".format(user))

            for item in cart:
                order_item = OrderItem.objects.create(
                    order=order, products=item['product'], price=item['price'], quantity=item['quantity'])
                order_item.products.stock -= item['quantity']
                order_item.products.on_sale += item['quantity']
                order_item.products.save()
                order_item.save()

            # clear cart
            cart.clear()
            return redirect(reverse('payment:pay-payment', kwargs={'pk': order.pk}))


def order_history(request):
    return render(request, 'order/order_history.html')


class OrderHistory(LoginRequiredMixin, View):
    def get(self, request):
        active_order = Order.objects.filter(is_ordered=True, user=request.user)
        order_history = Order.objects.filter(is_ordered=True, is_delivered=True, user=request.user)
        pending_order = Order.objects.filter(is_ordered=False, user=request.user)
        context = {
            'active_order': active_order,
            'order_history': order_history,
            'pending_order': pending_order,
        }
        return render(request, 'order/order_history.html', context)
