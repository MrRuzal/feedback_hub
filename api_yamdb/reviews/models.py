from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from rest_framework.response import Pesponse


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'пользователь'
        MODERATOR = 'moderator', 'модератор'
        ADMIN = 'admin', 'администратор'

    username = models.TextField(
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\z',
                code=Response(status=status.HTTP_400_BAD_REQUEST),
            )
        ],
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роли',
    )
