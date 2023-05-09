from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from rest_framework import status
from rest_framework.response import Response


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


class Categories(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                code=Response(status=status.HTTP_400_BAD_REQUEST)
            )
        ]
    )


class Genres(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        validators=[
            RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')
        ]
    )


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    pub_date = models.IntegerField()
    description = models.TextField(
        verbose_name='Описание произведения'
    )
    categories = models.ForeignKey(
        Categories,
        related_name='title',
        on_delete=models.CASCADE,
    )
    genres = models.ForeignKey(
        Genres,
        related_name='title',
        on_delete=models.CASCADE
    )
