from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from rest_framework import status
from django.contrib.auth.models import User


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'пользователь'
        MODERATOR = 'moderator', 'модератор'
        ADMIN = 'admin', 'администратор'

    username = models.TextField(
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username must be in the format: '
                'litters,numbers, @, ., +, -,',
                code=status.HTTP_400_BAD_REQUEST,
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


class Categorie(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                code=status.HTTP_400_BAD_REQUEST,
            )
        ],
    )


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                code=status.HTTP_400_BAD_REQUEST,
            )
        ],
    )


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='название',
    )
    year = models.IntegerField(verbose_name='год выпуска')
    description = models.TextField(verbose_name='описание', blank=True)
    categories = models.ForeignKey(
        Categorie,
        related_name='title',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='title',
        blank=True,
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def str(self):
        return f'{self.title} {self.genre}'
