from django.urls import include, path
from rest_framework import routers

from .views import TitlesViewSet, GenreViewSet, CategoryViewSet
from users.views import UserViewSet


app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitlesViewSet, basename='titles')
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
