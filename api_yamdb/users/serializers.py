from django.conf import settings
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import (CharField,
                                        EmailField,
                                        ModelSerializer,
                                        Serializer,
                                        ValidationError)
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(ModelSerializer):
    username = CharField(
        max_length=settings.USER_FIELD_LEN,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="Имя пользователя не соответствует, "
                        "можно использовать только буквы, "
                        "цифры и нижнее подчеркивания."),
            UniqueValidator(queryset=User.objects.all())
        ],
    )

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

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        if not username:
            raise ValidationError('Не указано поле username')

        try:
            user = get_object_or_404(User, username=username)
        except User.DoesNotExist:
            return Response(f'Пользователь {username} не найден',
                            status=status.HTTP_404_NOT_FOUND)

        if user.confirmation_code != confirmation_code:
            raise ValidationError('Неверный код подтверждения')

        return data


class SignUpSerializer(ModelSerializer):
    email = EmailField(max_length=settings.USER_FIELD_LEN)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Электронный адрес уже существует')

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(f'Пользователь "{username}" уже существует')

        if username.lower() == 'me':
            raise ValidationError('Нельзя использовать имя пользователя "me"')

        if username.lower() == 'admin':
            raise ValidationError(
                'Нельзя использовать имя пользователя "admin"'
            )

        return data
