from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, max_length=128)
