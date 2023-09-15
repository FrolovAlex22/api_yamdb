from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdmin
from users.models import User
from users.utils import sender_confirmation_code

from users.serializers import (GetTokenSerializer,
                               SignUpSerializer,
                               UserMeSerializer,
                               UserSerializer)


class UserViewSet(ModelViewSet):
    """
    Пользователи.

    Получение списка всех отзывов: Доступно без токена
        GET: /users/
    Добавить нового пользователя: Администратор.
        POST: /users/
    Получить пользователя по username: Администратор.
        GET: /users/{username}/
    Изменить данные пользователя по username: Администратор.
        PATCH: /users/{username}/
    Удалить пользователя по username: Администратор.
        DELETE: /users/{username}/
    Получить данные своей учетной записи: Любой авторизованный пользователь.
        GET: /users/me/
    Изменить данные своей учетной записи: Любой авторизованный пользователь.
        PATCH: /users/me/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    filter_backends = (SearchFilter,)
    permission_classes = (IsAuthenticated, IsAdmin)
    http_method_names = ('get', 'post', 'path', 'delete', 'patch')
    lookup_field = 'username'

    @action(detail=False,
            methods=['GET', 'PATCH'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=HTTP_200_OK)

        serializer = UserMeSerializer(request.user,
                                      data=request.data,
                                      partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class SignupView(APIView):
    """
    Регистрация нового пользователя.

    Получить код подтверждения на переданный email: Доступно без токена.
        POST: /auth/signup/
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(username=username, email=email).exists():
            sender_confirmation_code(request)
            return Response(request.data, status=HTTP_200_OK)

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        sender_confirmation_code(request)
        return Response(serializer.data, status=HTTP_200_OK)


class GetTokenView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            token = AccessToken.for_user(user)
            return Response(token, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
