from django.utils import timezone
from rest_framework.serializers import ValidationError


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError(
            f'Год не может быть больше чем {timezone.now().year}'
            f'Вы ввели {year}'
        )


def validate_username(value):
    """Убедитесь, что имя пользователя не равно 'me'."""
    if value == 'me':
        raise ValidationError("Username 'me' is not allowed.")
    return value
