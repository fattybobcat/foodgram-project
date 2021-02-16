from django.views.generic import CreateView
from .forms import RegisterForm
from django.urls import reverse_lazy

class SignUp(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("signup")
    template_name = "signup.html"