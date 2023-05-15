from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    MAX_CHAR_LENGTH,
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User,
)
from reviews.validators import validate_username, validate_username_bad_sign
from reviews.models import MAX_EMAIL_LENGTH

MAX_CHAR_LENGTH = 150


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

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
        read_only_fields = ('__all__',)


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
            'description',
            'genre',
            'category',
        )
        model = Title

    def to_representation(self, instance):
        return TitleListSerializer(instance).data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'bio',
            'role',
            'first_name',
            'last_name',
        )
        model = User


class UserRoleSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_CHAR_LENGTH,
        validators=[validate_username, validate_username_bad_sign],
    )
    confirmation_code = serializers.CharField()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_CHAR_LENGTH,
        validators=[validate_username, validate_username_bad_sign],
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
    )


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
        """
        request = self.context.get('request')
        if not request.method == 'POST':
            return attrs

        title_id = self.context.get('view').kwargs['title_id']
        author = self.context.get('request').user
        if Review.objects.filter(author=author, title=title_id).exists():
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
