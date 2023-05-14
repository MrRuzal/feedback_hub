from django.contrib.auth.models import AbstractUser, User
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from rest_framework import status

from api.validators import validate_username, validet_year


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'пользователь'
        MODERATOR = 'moderator', 'модератор'
        ADMIN = 'admin', 'администратор'

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='150 characters or fewer. '
                'Letters, digits and @/./+/-/_ only',
                code=status.HTTP_400_BAD_REQUEST,
            ),
            validate_username,
        ],
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роли',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)


class NameAndSlugAbstarct(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)


class Category(NameAndSlugAbstarct):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameAndSlugAbstarct):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='название',
    )
    year = models.SmallIntegerField(
        validators=(validet_year,), verbose_name='Год выпуска'
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    category = models.ForeignKey(
        Category,
        related_name='title',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='title',
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведения'
        verbose_name_plural = 'Произведении'
        ordering = ('name',)


class AuthorTextPubDate(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def str(self):
        return self.text


class Review(AuthorTextPubDate):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE
    )
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                name='unique_review', fields=['author', 'title']
            )
        ]


class Comment(AuthorTextPubDate):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Коментария'
        verbose_name_plural = 'Коментарии'


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def str(self):
        return f'{self.title} {self.genre}'
