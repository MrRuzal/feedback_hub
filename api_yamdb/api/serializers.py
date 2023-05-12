from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.db import IntegrityError

from reviews.models import (
    Title,
    Category,
    Genre,
    Review,
    Comment,
    User,
)
from api.validators import validate_username, validate_username_bad_sign

USER_FIELDS = ['username', 'email', 'bio', 'role', 'first_name', 'last_name']


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )
        model = Title


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = USER_FIELDS
        model = User


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = USER_FIELDS
        model = User
        read_only_fields = ['role']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    confirmation_code = serializers.CharField(required=True)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username, validate_username_bad_sign],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def create(self, validated_data):
        try:
            user = User.objects.get_or_create(**validated_data)[0]
        except IntegrityError:
            raise serializers.ValidationError('Такая запись уже существует')
        return user

    class Meta:
        fields = ('username', 'email')
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review (Ревью произведений).
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        """
        Проверяет, что пользователь
        не оставляет отзыв на одно произведение дважды.
        Args:
            attrs (dict): Входные данные, которые требуется проверить.
        Raises:
            serializers.ValidationError: Выбрасывается, если пользователь уже
            оставил отзыв с указанным title_id.
        Returns:
            dict: Проверенные и валидные данные.
        """
        request = self.context['request']
        if request.method == 'POST':
            title_id = request.parser_context['kwargs'].get('title_id')
            user = request.user
            if user.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment (Комментарии).
    """

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
