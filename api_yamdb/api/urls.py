from django.urls import include, path
from rest_framework import routers

# from .views import 

app_name = 'api'

v1_router = routers.DefaultRouter()


urlpatterns = [
    path('', include(v1_router.urls)),
]
