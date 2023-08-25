from django.urls import include, path
from rest_framework import routers

# from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

v1_router = routers.DefaultRouter()
# v1_router.register(r'follow', FollowViewSet, basename='follows')


urlpatterns = [
    path('', include(v1_router.urls)),
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
]
