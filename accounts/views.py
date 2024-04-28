from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm 

class SignUpView(CreateView):
    form_class = CustomUserCreationForm  
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def logout(request):
    django_logout(request)
    return redirect('/')
