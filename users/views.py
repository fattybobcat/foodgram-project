from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .forms import RegisterForm
from django.shortcuts import get_object_or_404, render, redirect


class SignUp(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "reg.html"

def register(request):
    """ Представление формы регистрации пользователя. """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user.refresh_from_db()

            return render(request, 'reg.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'reg.html', {
        'user_form': user_form,
    })