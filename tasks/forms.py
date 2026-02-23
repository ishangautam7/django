from django import forms
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
