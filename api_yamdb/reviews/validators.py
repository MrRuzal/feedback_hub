from django.conf import settings
import re

from django.utils import timezone
from rest_framework.serializers import ValidationError


def validate_username(value):
    """Убедитесь, что имя пользователя не равно зарезервированным никам."""
    if value in settings.RESERVED_USERNAMES_ME:
        raise ValidationError(f"Имя пользователя '{value}' недопустимо.")
    return value


def validate_username_bad_sign(value):
    """Валидация запрета недопустимых символов в имени пользователя"""
    invalid_chars = re.findall(r'[^\w.@+-]', value)
    if invalid_chars:
        raise ValidationError(
            f"Имя пользователя содержит недопустимые символы: "
            f"{''.join(set(invalid_chars))}"
        )
    return value


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError(
            f'Год не может быть больше чем {timezone.now().year}'
            f'Вы ввели {year}'
        )
