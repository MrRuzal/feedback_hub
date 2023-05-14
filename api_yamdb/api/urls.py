from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewVeiewSet,
    SignupView,
    TitleVewSet,
    TokenView,
    UserViewSet,
)

router_v1 = DefaultRouter()
router_v1.register('titles', TitleVewSet, basename='titles')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewVeiewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='commments',
)
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
]
