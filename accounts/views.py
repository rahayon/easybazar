from django.http.response import HttpResponseRedirect
from accounts.forms import LoginForm, RegisterForm, ProfileForm
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
#from .models import CustomUser
from django.contrib.auth import get_user_model


class Register(SuccessMessageMixin, CreateView):
    template_name = 'accounts/signup.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')
    success_message = "Your Account was created successfully"

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
