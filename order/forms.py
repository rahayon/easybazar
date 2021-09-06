from django import forms
from django.core.checks import messages
from .models import Order

class OrderCreationForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'address', 'city', 'mobile_number',)
        

class RefundForm(forms.Form):
    ref_code = forms.CharField(max_length=30)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    mobile = forms.CharField(max_length=11)
