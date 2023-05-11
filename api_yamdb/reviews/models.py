from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from rest_framework import status
from django.contrib.auth.models import User
from api.validators import validate_username


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


class Category(models.Model):
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
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )
    count_review = models.IntegerField('Колличество оевью', default=0)
    year = models.IntegerField(verbose_name='год выпуска')
    description = models.TextField(verbose_name='описание', blank=True)
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


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата ревью', auto_now_add=True, db_index=True
    )
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[MinLengthValidator(1), MaxLengthValidator(10)],
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                name='unique_review', fields=['author', 'title']
            )
        ]

    def calculate_rating(self):
        avg_rating = self.comments.aggregate(Avg('score'))['score__avg']
        self.rating = round(avg_rating) if avg_rating is not None else 0
        self.save()


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата коммента', auto_now_add=True, db_index=True
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def str(self):
        return f'{self.title} {self.genre}'
