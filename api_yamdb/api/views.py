from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken


from reviews.models import Title, Categorie, Genre, User, Review, Comment
from api.serializers import (
    TitleSerializer,
    GenresSerializer,
    CategoriesSerializer,
    ReviewSerializer,
    CommentSerializer,
)

from reviews.models import Title, Categorie, Genre, User, Review, Comment
from api.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    search_fields = ('username',)
    filter_backends = (SearchFilter,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def get_patch(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserRoleSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserRoleSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


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


class SignupView(CreateAPIView):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        confirmation_code = default_token_generator.make_token(user)
        email_data = {
            'subject': 'Добро пожаловать на наш сайт!',
            'message': f'Your confirmation_code: {confirmation_code}',
            'from_email': settings.TOKEN_EMAIL,
            'recipient_list': [user.email],
        }
        send_mail(**email_data)

        return Response({'email': user.email, 'username': user.username})


class TokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'],
        )
        if not default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
        ):
            raise ValidationError('Неверный код подтверждения.')
        token = AccessToken().for_user(user)
        return Response({'token': str(token)})
