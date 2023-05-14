from django.contrib.auth.models import AbstractUser
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

    def if_user(self):
        return self.role == 'user'

    def is_admin(self):
        return self.role == 'admin'

    def is_moredator(self):
        return self.role == 'moderator'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class NameAndSlugAbstarct(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(NameAndSlugAbstarct):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(NameAndSlugAbstarct):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


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

    def __str__(self):
        return self.name


class AbstractReviewComment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)ss'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата ревью',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class Review(AbstractReviewComment):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
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

    def __str__(self):
        return f'{self.author.username} {self.title}'


class Comment(AbstractReviewComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = 'Коментария'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return f'{self.author.username} {self.review}'


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
