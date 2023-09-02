import datetime as dt

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from reviews.models import Category, Genre, Titles


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


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для TitlesViewSet"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
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
