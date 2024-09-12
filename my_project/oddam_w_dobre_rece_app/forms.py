from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User




class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, label='Imię', required=True)
    surname = forms.CharField(max_length=100, label='Nazwisko', required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło', required=True)

    def clean_password2(self):
        # Sprawdzamy, czy hasła się zgadzają
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Hasła muszą być takie same.")
        return password2

    def clean_email(self):
        # Sprawdzamy, czy adres email już istnieje
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ten email jest już zajęty.")
        return email
