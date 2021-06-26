from django import forms
from .models import DeliveryLocation
from  cart.cart import Cart



class  DeliveryForm(forms.Form):
    delivery = forms.ModelChoiceField(label='', queryset=DeliveryLocation.objects.all(), empty_label=None)


