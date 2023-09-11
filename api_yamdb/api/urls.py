from django.urls import include, path
from rest_framework import routers

from api.views import (
    CommentViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    ReviewViewSet
)
from users.views import UserViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitleViewSet, basename='title')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'users', UserViewSet, basename='users')
# v1_router.register(r'follow', FollowViewSet, basename='follows')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include('users.urls')),
    path('v1/', include(v1_router.urls))
]
