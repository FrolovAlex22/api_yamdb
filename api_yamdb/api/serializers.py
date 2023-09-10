
from collections import OrderedDict
import datetime as dt

from rest_framework import serializers
from rest_framework.serializers import (CurrentUserDefault,
                                        ModelSerializer,
                                        SlugRelatedField,
                                        ValidationError)

from reviews.models import Category, Genre, Titles, Comment, Review


class ReviewSerializer(ModelSerializer):
    """Сериалайзер модели Review."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Защита от повторов отзыва от пользователя."""
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise ValidationError('Отзыв уже был ранее')
        return data


class CommentSerializer(ModelSerializer):
    """Сериалайзер модели Comment."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для CategoryViewSet"""

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate(self, data):
        name = data.get('name')
        slug = data.get('slug')
        if self.context['request'].method == 'POST':
            if not name:
                raise ValidationError('Не указано поле name')
            if not slug:
                raise ValidationError('Не указано поле slug')
        return data


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для GenreViewSet"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate(self, data):
        name = data.get('name')
        slug = data.get('slug')
        if self.context['request'].method == 'POST':
            if not name:
                raise ValidationError('Не указано поле name')
            if not slug:
                raise ValidationError('Не указано поле slug')
        return data


class TitlesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для TitlesViewSet"""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для TitlesViewSet"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles

    def validate(self, data):
        name = data.get('name')
        genre = data.get('genre')
        category = data.get('category')
        if self.context['request'].method == 'POST':
            if not name:
                raise ValidationError('Не указано поле name')
            if not genre:
                raise ValidationError('Не указано поле genre')
            if not category:
                raise ValidationError('Не указано поле category')
        return data

    def validate_year(self, value):
        if not value:
            raise ValidationError(
                'Не указано поле year'
            )
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска произведения дожен быть раньше этого года'
            )
        return value
