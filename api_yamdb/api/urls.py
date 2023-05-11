from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, GenresViewSet,
                    TitleVewSet, CommentViewSet, ReviewVeiewSet, TokenView)

router_v1 = DefaultRouter()
router_v1.register('titles', TitleVewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewVeiewSet,
                   basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='commments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]