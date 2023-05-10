from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action

from api.serializers import (
    TitleSerializer,
    GenresSerializer,
    CategoriesSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from reviews.models import Titles, Categories, Genres, User

from api.serializers import (
    TitleSerializer,
    GenresSerializer,
    CategoriesSerializer,
    UserSerializer,
    UserRoleSerializer,
    TokenSerializer,
    SignupSerializer,
)
from api.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsAdmin
    lookup_field = 'username'
    search_fields = ('username',)

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
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class ReviewVeiewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')

        title = get_object_or_404(Titles, id=title_id)
        review = title.reviews.filter(id=review_id).first()

        if review is None:
            raise ValueError('У произведения нет такого отзыва')

        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')

        title = get_object_or_404(Titles, id=title_id)
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


class SignupView(CreateAPIView):
    permission_classes = [AllowAny]

    def send_email(self, email):
        email = EmailMessage(
            subject=email['email_subject'],
            body=email['email_body'],
            to=[email['to_email']],
        )
        email.send()

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        email_body = 'Добро пожаловать на наш сайт!'
        email_data = {
            'email_subject': 'Добро пожаловать на наш сайт!',
            'email_body': email_body,
            'to_email': user.email,
        }
        self.send_email(email_data)

        return Response(
            {'email': user.email, 'username': user.username},
            status=status.HTTP_201_CREATED,
        )
