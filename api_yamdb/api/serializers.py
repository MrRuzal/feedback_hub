from rest_framework import serializers

from reviews.models import Titles, Categories, Genres, User


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Titles


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
