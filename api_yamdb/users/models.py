from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import UsernameValidator


class User(AbstractUser):
    USER = settings.USER
    MODERATOR = settings.MODERATOR
    ADMIN = settings.ADMIN

    CHOICES_ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.USER_FIELD_LEN,
        unique=True,
        validators=[UsernameValidator]
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=settings.USER_FIELD_LEN
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.USER_FIELD_LEN,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.USER_FIELD_LEN,
        blank=True
    )
    bio = models.TextField(
        'О себе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        default=USER,
        max_length=settings.USER_FIELD_LEN,
        choices=CHOICES_ROLE
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.USER_FIELD_LEN,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    def __str__(self):
        return self.username
