from django import forms
from django.forms import widgets
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment_type', 'transaction_id', 'mobile_number')
        
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_type'].empty_label = None
        self.fields['transaction_id'].required = False
        self.fields['transaction_id'].widget.attrs.update({'placeholder': 'Transaction ID', 'class':'form-control'})
        self.fields['mobile_number'].required = False
        self.fields['mobile_number'].widget.attrs.update({'placeholder': '01*********'})


        
    
