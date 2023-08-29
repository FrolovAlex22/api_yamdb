from django.conf import settings
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
from user.models import User
from user.utils import sender_confirmation_code

from user.serializers import (GetTokenSerializer,
                              SignupSerializer,
                              UserMeSerializer,
                              UserSerializer)


class UserViewSet(ModelViewSet):
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
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            user = get_object_or_404(User, username=username)
            serializer = SignupSerializer(user,
                                          data=request.data,
                                          partial=True)
            serializer.is_valid(raise_exception=True)

            if serializer.validated_data['email'] != user.email:
                return Response('Неверный электронный адрес',
                                status=HTTP_400_BAD_REQUEST)
            serializer.save(raise_exception=True)
            sender_confirmation_code(request)
            return Response(serializer.data, status=HTTP_200_OK)

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(
                email=serializer.validated_data['email']).exists():
            return Response('Электронный адрес уже существует',
                            status=HTTP_400_BAD_REQUEST)

        if serializer.validated_data['username'] != settings.ADMIN:
            serializer.save()
            sender_confirmation_code(request)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response('Нельзя использовать имя пользователя "admin"',
                        status=HTTP_400_BAD_REQUEST)


class GetTokenView(TokenObtainPairView):
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response('Неверный код подтверждения',
                            status=HTTP_400_BAD_REQUEST)
        token = f'{AccessToken.for_user(user)}'
        return Response(token, status=HTTP_200_OK)
