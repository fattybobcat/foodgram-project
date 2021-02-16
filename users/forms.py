from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterForm(UserCreationForm):
    """Форма регистрации"""
    email = forms.EmailField(max_length=254, help_text='Это поле обязательно')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)