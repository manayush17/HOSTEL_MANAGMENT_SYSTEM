from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    is_student = forms.BooleanField(required=False, label="Register as Student")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_student']
