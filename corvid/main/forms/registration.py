from django import forms
from main.models import User


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}
