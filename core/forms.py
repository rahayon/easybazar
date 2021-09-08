from django import forms
from django.forms import fields
from .models import ContactUs
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'mobile', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Your Mobile', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message', 'rwos': 4, 'class': 'form-control'})
        }
        
