from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Categorie, Genre, User, GenreTitle


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
        fields = '__all__'
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=genre, title=title)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
