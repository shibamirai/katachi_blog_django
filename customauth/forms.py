from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "autofocus": True,
            "class": "form-control"
        })
    )

    password = forms.CharField(
        label = 'パスワード',
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )
