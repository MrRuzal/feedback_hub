import re

from rest_framework.serializers import ValidationError
from django.utils import timezone


def validate_username(value):
    """Убедитесь, что имя пользователя не равно 'me'."""
    if value.lower() == 'me':
        raise ValidationError("Username 'me' is not allowed.")
    return value


def validate_username_bad_sign(value):
    """Валидация запрета недопустимых символов"""
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            "Имя пользователя содержит" "недопустимые символы"
        )
    return value


def validet_year(year):
    if year > timezone.now().year:
        raise ValidationError('Такого года быть не может')
