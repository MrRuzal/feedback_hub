from rest_framework import serializers
import re


def validate_username(value):
    """Убедитесь, что имя пользователя не равно 'me'."""
    if value.lower() == 'me':
        raise serializers.ValidationError("Username 'me' is not allowed.")
    return value


def validate_username_bad_sign(value):
    """Валидация запрета недопустимых символов"""
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise serializers.ValidationError(
            "Имя пользователя содержит" "недопустимые символы"
        )
    return value
