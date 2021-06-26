from order.models import Order
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from .forms import PaymentForm
from .models import PaymentType
from django.contrib import messages
# Create your views here.

class PayPaymentView(View):
    def get(self, request, pk, *args, **kwargs):
        pay_form = PaymentForm()
        payment_type = PaymentType.objects.exclude(merchant_number='')
        return render(request, 'payment/pay.html',{'pay_form': pay_form,'payment': payment_type})

    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        form = PaymentForm(request.POST)
        if form.is_valid():
            pay=form.save(commit=False)
            pay.order = order
            pay.save()
            messages.success(request,'Your Payment is completed.Your order No is {}. we will inform you 2-3 hours after verifying'.format(pay.order))
            return redirect('core:home')
            
