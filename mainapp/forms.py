from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2', 'last_name', 'first_name', 'middle_name', 'phone_number', 'email']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'phone_number': 'Номер телефона',
            'email': 'Электронная почта',
        }
        # валидаторы добавить

class RealtorRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2', 'last_name', 'first_name', 'middle_name', 'commission', 'email']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'commission': 'Доля от комиссии',
            'email': 'Электронная почта',
        }
