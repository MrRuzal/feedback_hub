from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (
    IsAdmin,
    IsAdminAuthorModeratorOrReadOnly,
    IsAdminOrReadOnly,
)
from api.serializers import (
    CategoriesSerializer,
    CommentSerializer,
    GenresSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleListSerializer,
    TitleSerializer,
    TokenSerializer,
    UserRoleSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Title, User


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
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return TitleListSerializer


class ListCreateDeletMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    ...


class CategoriesViewSet(ListCreateDeletMixin):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(ListCreateDeletMixin):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class ReviewVeiewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]

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
            'message': f'Ваш confirmation_code: {confirmation_code}',
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
