from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterForm(UserCreationForm):
    """Форма регистрации"""
   # email = forms.EmailField(max_length=254, help_text='Это поле обязательно')
   # username = forms.CharField(max_length=150, label='Логин')
   # password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
   # password2 = forms.CharField(
   #     label='Повторите пароль', widget=forms.PasswordInput)
   # error_css_class = 'error'

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ("first_name", "username", "email")
        required_fields = ("first_name", "username", "email")