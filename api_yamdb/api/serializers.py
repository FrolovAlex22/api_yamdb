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
    # User
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
        fields = '__all__'
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

# Мы не можем разобраться с вашим замечанием: Рекомендуется использовать
# related_name вместо фильтра для улучшения
# читаемости кода и более простого доступа к связанным объектам.

# Насколько я понял в связке(Title -> Review < - User) связаться ч/з
# related_name с указанными в фильтре параметрами можно только через модель
# Review. При поиске ч/з модель User я могу получить список всех ревью
# пользователя, но как найти среди этих ревью то что к нашему посту.
# так же ч/з модель Title я могу получить список всех ревью произведения,
# но как найти среди этих ревью то что к нашему пользователю.
# Напрашиваеться вывод что вся эта информация есть у модели review

    # def validate(self, data):
    #     author = self.context['request'].user
    #     title_id = self.context['view'].kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     if author == title.reviews.author:
    #         raise ValidationError('Отзыв уже был ранее')
    #     return data

# выдает ошибку: TypeError: all() got an unexpected keyword argument 'author'
# тут я не могу добраться до поля автор ч/з related_name

    # def validate(self, data: OrderedDict) -> OrderedDict:
    #     """Защита от повторов отзыва от пользователя."""
    #     if self.context['request'].method != 'POST':
    #         return data
    #     author = self.context['request'].user
    #     title_id = self.context['view'].kwargs.get('title_id')
    #     user = User.objects.get(username=author)
    #     if user.reviews.get(title=title_id).exists():
    #         raise ValidationError('Отзыв уже был ранее')

    #     return data

# выдает ошибку: reviews.models.Review.DoesNotExist: Review matching query does
# not exist.
# Тут я зашел немного с другой стороны, ищу в списке ревью нашего
# пользователя конкретное произваедение, и если оно существует вывожу ошибку.
# но его нет

    # def validate(self, data: OrderedDict) -> OrderedDict:
    #     """Защита от повторов отзыва от пользователя."""
    #     if self.context['request'].method != 'POST':
    #         return data
    #     author = self.context['request'].user
    #     user = User.objects.get(username=author)
    #     title_id = self.context['view'].kwargs.get('title_id')
    #     if Review.objects.get(title=title_id).exists():
    #         if user.reviews.title.get(title=title_id):
    #             raise ValidationError('Отзыв уже был ранее')
    #     return data

# выдает ошибку: reviews.models.Review.DoesNotExist: Review matching query does
# not exist.
# Тут пытаюсь сперва убедится что для произведения есть хоть
# какое то ревью и уже если оно существует сверить ч/з модель User посредством
# related_name проверить могу ли я дотягуться до поля title и извлечь его
# значение методом get.# Не уверен таким способом можно извлекать значение.
# К тому же в# поле title# указан serializers.SlugRelatedField в котором
# отмечено поле 'name'.# Но оставил этот вариант как пример того что
# рассматривали как решение.

# Ввиду нашей не опытности и пока еще шаблонного мышления :D
# Просим дополнительную подсказку.


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
