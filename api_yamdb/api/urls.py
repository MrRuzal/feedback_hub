from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleVewSet,
    UserViewSet,
    TokenView,
    SignupView,
)


router_v1 = DefaultRouter()
router_v1.register('titles', TitleVewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
]
