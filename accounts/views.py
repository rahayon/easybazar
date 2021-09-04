from django.http.response import HttpResponseRedirect
from accounts.forms import AddressForm, LoginForm, RegisterForm, ProfileForm
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.contrib.auth.hashers import make_password
#from .models import CustomUser
from django.contrib.auth import get_user_model


class Register(View):


    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'accounts/signup.html', {'form': register_form,})

    def post(self, request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            print("form valid")
            name = register_form.cleaned_data.get('full_name')
            address = register_form.cleaned_data.get('address')
            mobile_no = register_form.cleaned_data.get('mobile')
            email = register_form.cleaned_data.get('email')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            
            if CustomUser.objects.filter(mobile=mobile_no).exists():
                messages.error(
                    request, "Customer with this  {0} number is already exists".format(mobile_no))
                return redirect('accounts:signup')
            else:
                if password1 != password2:
                    messages.error(request, "Password does not match")
                    return redirect('accounts:signup')

                else:
                    password_hash = make_password(password2)
                    user = CustomUser.objects.create(mobile=mobile_no, password=password_hash)
                    

                if email:
                    user.email = email
                    user.save()

                user.profile.full_name = name
                user.profile.address = address
                user.profile.save()
                user.save()
                
                login(request, user)
                messages.success(
                    request, "Account for {0} is created Successfully".format(user))
                return redirect('accounts:profile')
            
        else:
            
            messages.error(request, register_form.errors)
            return redirect('accounts:signup')

class Login(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return render(request, 'accounts/login.html', {'form': form})
        else:
            return redirect('core:home')

    def post(self, request):
        if not request.user.is_authenticated:
            form = LoginForm(request.POST)
            if form.is_valid():
                mobile = form.cleaned_data.get('mobile')
                password = form.cleaned_data.get('password')
                #return HttpResponse("form valid")
                user = authenticate(mobile=mobile, password=password)
                if user:

                    login(request, user)
                    print("successfully login")
                    messages.success(request, "Logged in Successfully")
                    next_url = request.POST.get('next')
                    print(next_url)
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('core:home')
                else:
                    messages.warning(request, "Mobile or Password is incorrect")
                    return redirect('accounts:login')
            else:
                messages.error(request, "Mobile or Password is incorrect")
                return redirect('accounts:login')
        else:
            return redirect('core:home')


class Logout(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, "Logged Out Successfully")
        return redirect("accounts:login")

class Profile(LoginRequiredMixin, View):
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile is updated successfully')
            return redirect('accounts:profile')
        else:
            messages.warning()(request, 'Profile is not updated')
            return render(request, self.template_name, {'form': form})
