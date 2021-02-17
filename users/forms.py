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


class CreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'username', 'email']