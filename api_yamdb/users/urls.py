from django.urls import path

from users.views import GetTokenView, SignupView

urlpatterns = [
    path('auth/token/', GetTokenView.as_view(), name='get_token'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
]
