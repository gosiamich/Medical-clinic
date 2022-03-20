from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from .forms import LoginForm, CreateUserForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'doctor_app/form.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                redirect_url = request.GET.get('next', 'index')
                return redirect(redirect_url)
        return render(request, 'doctor_app/form.html', {'form': form, 'message':'Try again..'})


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class RegistrationView(View):

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'doctor_app/form.html', {'form':form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("index")
        return render(request, 'doctor_app/form.html', {'form': form})

