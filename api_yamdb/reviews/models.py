from django.db import models
from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator
)

from users.models import User


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug',
        validators=[RegexValidator(
            regex=r'^[0-9a-zA-Z]*$',
            message='Поле "slug" должно состоять из символов:[0-9a-zA-Z]'
        )
        ]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='TitlesGenre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='category',
    )

    class Meta:
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name


class TitlesGenre(models.Model):
    titles = models.ForeignKey(Titles, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.titles} {self.genre}'


class Review(models.Model):
    min_rating = 1
    max_rating = 10
    title = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        default=1,
        validators=[
            MinValueValidator(min_rating, 'Возможны значения по шкале от 1 до 10'),
            MaxValueValidator(max_rating, 'Возможны значения по шкале от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name = 'Дата'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author')


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name = 'Дата'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
