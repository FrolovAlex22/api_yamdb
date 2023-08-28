from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import (CharField,
                                        EmailField,
                                        ModelSerializer,
                                        Serializer,
                                        ValidationError)

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'bio')


class UserMeSerializer(UserSerializer):
    role = CharField(read_only=True)


class GetTokenSerializer(Serializer):
    username = CharField(max_length=settings.USER_FIELD_LEN)
    confirmation_code = CharField(max_length=settings.USER_FIELD_LEN)

    def validate_username(self, data):
        username = data.get('username')

        if not username:
            raise ValidationError('Не указано поле username')

        try:
            user = get_object_or_404(User, username=username)
        except User.DoesNotExist:
            raise ValidationError(f'Пользователь {username} не найден')

        if user.username != username:
            return Response(
                {'detail': 'Некорректные данные'},
                status=status.HTTP_404_NOT_FOUND
            )

        return data

    def validate_confirmation_code(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if user.confirmation_code != confirmation_code:
            ValidationError('Неверный код подтверждения')

        return data


class SignUpSerializer(ModelSerializer):
    email = EmailField(max_length=settings.USER_FIELD_LEN)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Нельзя использовать имя пользователя "me"')
        return value
