from decimal import Decimal
from delivery.models import DeliveryType
from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import OrderCreationForm, RefundForm
from cart.cart import Cart
from .models import Order, OrderItem, Refund
from django.urls import reverse
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import string

# Create your views here.

def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=20))
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
            order.ref_code = create_ref_code()
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
        active_order = Order.objects.filter(order_status='Confirmed', user=request.user)
        order_history = Order.objects.filter(order_status='Delivered', user=request.user)
        pending_order = Order.objects.filter(order_status='Pending', user=request.user)
        context = {
            'active_order': active_order,
            'order_history': order_history,
            'pending_order': pending_order,
        }
        return render(request, 'order/order_history.html', context)


class RefundRequest(View):
    def get(self, request):
        form = RefundForm()
        return render(request, 'order/refund_request.html', {'form':form})
    def post(self, request):
        form = RefundForm(request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            mobile = form.cleaned_data.get('mobile')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_status = 'Requested'
                order.save()
            
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.mobile = mobile
                refund.save()
                messages.info(request, "Your refund requests was received")
                return redirect('core:home')

            except Order.DoesNotExist:
                messages.info(request, "Your Order does not exists")
                return redirect('core:home')
            