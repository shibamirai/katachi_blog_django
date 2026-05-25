from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'body', 'category')
        widgets = {
            'title': forms.TextInput(attrs={
                "class": "form-control"
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            'body': forms.Textarea(attrs={
                "class": "form-control"
            }),
            'category': forms.Select(attrs={
                "class": "form-select"
            })
        }
