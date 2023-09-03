from collections import OrderedDict

from rest_framework.serializers import (CurrentUserDefault,
                                        ModelSerializer,
                                        SlugRelatedField, ValidationError)
from reviews.models import Comment, Review


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
