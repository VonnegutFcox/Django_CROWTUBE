# функция-валидатор:
from django.forms import forms


def validate_not_empty(value):
    # проверка "а заполнено ли поле?"
    if value == '':
        raise forms.ValidationError(
            'А кто поле будет заполнять, Пушкин?',
            params={'value': value},
        )