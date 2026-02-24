from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


class TaskForm(forms.ModelForm):
    """Django ModelForm for Task - handles form validation automatically"""

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'width:100%; padding:8px;',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'style': 'width:100%; padding:8px;',
                'rows': 4,
                'placeholder': 'Enter task description'
            }),
            'completed': forms.CheckboxInput(),
        }


class RegisterForm(UserCreationForm):
    """User registration form extending Django's built-in UserCreationForm"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'style': 'width:100%; padding:8px;',
        'placeholder': 'Enter email'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

