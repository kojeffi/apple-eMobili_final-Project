# forms.py in user_auth app

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from user_auth.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
