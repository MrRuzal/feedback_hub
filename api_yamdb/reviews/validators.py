from django.utils import timezone
from rest_framework.serializers import ValidationError


def validet_year(year):
    if year > timezone.now().year:
        raise ValidationError('Такого года быть не может')


def validate_username(value):
    """Убедитесь, что имя пользователя не равно 'me'."""
    if value == 'me':
        raise ValidationError("Username 'me' is not allowed.")
    return value
