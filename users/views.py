from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, CreationForm
from django.shortcuts import get_object_or_404, render, redirect


class SignUp(CreateView):
    form_class = CreationForm
   # success_url = reverse_lazy("login")
    success_url = '/auth/login'
    template_name = "reg.html"

