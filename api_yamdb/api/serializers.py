from collections import OrderedDict

from rest_framework import serializers

from rest_framework.serializers import (
    CurrentUserDefault,
    ModelSerializer,
    SlugRelatedField,
    ValidationError
)

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


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


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для TitleViewSet"""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

    def get_rating(self, obj):
        return obj.rating


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для TitleViewSet"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title

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
        fields = (
            'id',
            'title',
            'text',
            'author',
            'score',
            'pub_date'
        )

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Защита от повторов отзыва от пользователя."""
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if author.reviews.filter(title__id=title_id):
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
        fields = (
            'id',
            'review',
            'author',
            'text',
            'pub_date'
        )
