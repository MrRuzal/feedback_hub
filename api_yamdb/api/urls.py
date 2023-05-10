from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TokenView


router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth_token/', TokenView.as_view(), name='token'),
]
