from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import 

router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]