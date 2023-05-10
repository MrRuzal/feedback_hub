from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TokenView

from .views import CategoriesViewSet, GenresViewSet, TitleVewSet

router_v1 = DefaultRouter()
router_v1.register('titles', TitleVewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth_token/', TokenView.as_view(), name='token'),
]
