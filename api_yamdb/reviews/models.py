from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'пользователь'
        MODERATOR = 'moderator', 'модератор'
        ADMIN = 'admin', 'администратор'

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10, choices=Role.choices, verbose_name='Роли'
    )
