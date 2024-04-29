from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'



def logout(request):
    django_logout(request)
    return redirect('/')
