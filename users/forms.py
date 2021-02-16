from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()
User = get_user_model()


class RegisterForm(UserCreationForm):
    """Форма регистрации"""

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ("first_name", "username", "email")
        required_fields = ("first_name", "username", "email")

class UserRegistrationForm(forms.ModelForm):
    """ Форма регистрации пользователя. """
    name = forms.CharField(max_length=150, label='Имя')
    email = forms.EmailField(max_length=200, label="Адрес электронной почты")
    username = forms.CharField(max_length=150, label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Повтор пароля', widget=forms.PasswordInput)
    error_css_class = 'error'

    class Meta:
        model = User
        fields = ("name", 'username', 'email', 'password', 'password2')

class CreationForm(UserCreationForm):

    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
