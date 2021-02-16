from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegisterForm


class SignUp(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"