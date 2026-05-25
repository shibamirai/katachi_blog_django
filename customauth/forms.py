from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


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


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'email')
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "form-control"
            }),
            'email': forms.EmailInput(attrs={
                "class": "form-control"
            })
        }
    
    password = forms.CharField(
        label = 'パスワード',
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )
    
    password_confirmation = forms.CharField(
        label = 'パスワード確認',
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    def clean_password_confirmation(self):
        # password_confirmation のバリデーション：password と一致しているか
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise ValidationError("パスワードが一致しません")
        return password_confirmation

    def save(self, commit=True):
        # まず Meta.fields で指定したフィールドで user を作成し、そこに password をセットしてから DB に登録する
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
