from django.shortcuts import render,redirect
from django.views.generic import View
from .models import DeliveryLocation, DeliveryType
from .forms import DeliveryForm

# Create your views here.
class DeliveryApply(View):

    def post(self, request):
        url =  request.META.get('HTTP_REFERER')
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.cleaned_data['delivery']
            print('Delivery type: ', delivery.id)
            try:
                request.session['delivery_id'] = delivery.id
                print(request.session['delivery_id'])

            except DeliveryLocation.DoesNotExist:
                request.session['delivery_id'] = 1
        return redirect(url)