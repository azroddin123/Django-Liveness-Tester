from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Form for the task model"""
    class Meta:
        model = Task
        fields = "__all__"