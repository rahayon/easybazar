from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import CustomUser
from accounts.models import UserProfile
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'profile_image', 'address', )
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


phone_regex = RegexValidator(
    regex=r'^01[13-9]\d{8}$', message="Phone number must be entered in the format: '01300000000'. Up to 11 digits allowed.")


class RegisterForm(forms.Form):
    full_name = forms.CharField(label='Full Name', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your Name'}))
    address = forms.CharField(label='Address', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}))
    mobile = forms.CharField(label='Mobile Number', validators=[phone_regex], max_length=11, widget=forms.TextInput(
        attrs={'placeholder': '01610000000'}))
    email = forms.EmailField(label='Email (for recovery account)', required=False, widget=forms.EmailInput(attrs={'placeholder': 'example@email.com'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address',)
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}), 
            }

class LoginForm(forms.Form):
    mobile = forms.CharField(validators=[
                             phone_regex], max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
