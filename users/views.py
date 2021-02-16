from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.shortcuts import get_object_or_404, render, redirect


class SignUp(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "reg.html"
