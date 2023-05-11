from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Title,
    Categorie,
    Genre,
    Review,
    Comment,
    User,
    GenreTitle,
)
from api.validators import validate_username, validate_username_bad_sign


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categorie


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genres = GenresSerializer(read_only=True, many=True)
    categories = SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'categories', 'genres')
        model = Title

    def create(self, validated_data):
        is_exists_genres = False
        if validated_data.get('genres'):
            genres = validated_data.pop('genres')
            is_exists_genres = True
        title = Title.objects.create(**validated_data)
        if is_exists_genres:
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(**genre)
                GenreTitle.objects.create(genre=current_genre, title=title)
        return title


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username_bad_sign],
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class UserRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username_bad_sign],
    )
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


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
        validators=[validate_username_bad_sign, validate_username_bad_sign],
    )
    email = serializers.EmailField(max_length=254)

    def create(self, validated_data):
        try:
            user = User.objects.get_or_create(
                username=validated_data['username'],
                email=validated_data['email'],
            )

        except KeyError as error:
            raise serializers.ValidationError(f"Отсутствующий ключ {error}")
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
        fields = '__all__'
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
