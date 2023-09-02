from django.urls import include, path
from rest_framework import routers

from .views import TitlesViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitlesViewSet, basename='titles')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
