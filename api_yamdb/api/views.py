from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .permissions import IsAdminAuthorModeratorOrReadOnly
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend


from reviews.models import Title, Category, Genre, User, Review, Comment
from api.serializers import (
    TitleSerializer,
    GenresSerializer,
    CategoriesSerializer,
    ReviewSerializer,
    CommentSerializer,
    TitleListSerializer,
)
from .serializers import TokenSerializer


class TitleVewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    search_fields = (
        'category__slug',
        'genre__slug',
        'name',
        'year',
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminAuthorModeratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewVeiewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_queryset(self):
        title = self.kwargs['title_id']
        return super().get_queryset.filter(title=title)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = Title.objects.get(id=title_id)
        score = serializer.score
        rating = title.rating
        if rating != None:
            count_review = title.count_review
            sum_score = rating * count_review
            new_rating = (score + sum_score) / (count_review + 1)
            data = {'count_review': count_review + 1, 'rating': new_rating}
        else:
            data = {'count_review': 1, 'rating': score}
        title_serializer = TitleSerializer(title, data=data, partial=True)
        if title_serializer.is_valid():
            title_serializer.save()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')

        title = get_object_or_404(Title, id=title_id)
        review = title.reviews.filter(id=review_id).first()

        if review is None:
            raise ValueError('У произведения нет такого отзыва')

        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')

        title = get_object_or_404(Title, id=title_id)
        review = title.reviews.filter(id=review_id).first()

        if review is None:
            raise ValueError('У произведения нет такого отзыва')

        serializer.save(author=self.request.user, review=review)


class TokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'],
            confirmation_code=serializer.validated_data['confirmation_code'],
        )
        token = AccessToken().for_user(user)
        return Response({'token': str(token)})
