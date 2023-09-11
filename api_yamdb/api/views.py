from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    BasePermission
)
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleGetSerializer
)
from reviews.models import Review, Category, Genre, Title

from .filters import TitleFilter
from .permissions import (
    IsAuthorModeratorAdminOrReadOnly,
    IsAdminOrSuperuser,
)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка).

    Получить список всех объектов: Доступно без токена
        GET: /titles/
    Добавить новое произведение: Администратор.
        POST: /titles/
    Информация о произведении: Доступно без токена
        GET: /titles/{titles_id}/
    Обновить информацию о произведении: Администратор
        PATCH: /titles/{titles_id}/
    Удалить произведение: Администратор.
        DELETE: /titles/{titles_id}/
    """

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self) -> BasePermission:
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()

    def get_serializer_class(self) -> ModelSerializer:
        if self.request.method == 'GET':
            return TitleGetSerializer
        return self.serializer_class


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Набор mixins для GenreViewSet, CategoryViewSet."""
    pass


class GenreViewSet(ListCreateDeleteViewSet):
    """
    Категории жанров.

    Получить список всех жанров: Доступно без токена
        GET: /genres/
    Добавить жанр: Администратор.
        POST /genres/
    Удалить жанр. Права доступа: Администратор.
        DELETE: /genres/{slug}/
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self) -> BasePermission:
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()


class CategoryViewSet(ListCreateDeleteViewSet):
    """
    Категории (типы) произведений.

    Получить список всех категорий: Доступно без токена
        GET: /categories/
    Создать категорию: Администратор.
        POST /categories/
    Удалить категорию: Администратор.
        DELETE: /categories/{slug}/
    """
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self) -> BasePermission:
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()


class ReviewViewSet(ModelViewSet):
    """
    Отзывы.

    Получение списка всех отзывов: Доступно без токена
        GET: /titles/{title_id}/reviews/
    Добавление нового отзыва: Аутентифицированные пользователи
        POST: /titles/{title_id}/reviews/
    Получение отзыва по id: Доступно без токена
        GET: /titles/{title_id}/reviews/{review_id}/
    Частичное обновление отзыва по id: Автор отзыва, модератор или админ
        PATCH: /titles/{title_id}/reviews/{review_id}/
    Удаление отзыва по id: Автор отзыва, модератор или админ
        DELETE: /titles/{title_id}/reviews/{review_id}/
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self) -> QuerySet:
        """Возвращает отзывы."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Создаёт отзыв в БД."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """
    Комментарии к отзывам

    Получение списка всех комментариев к отзыву: Доступно без токена
        GET: /titles/{title_id}/reviews/{review_id}/comments/
    Добавление комментария к отзыву: Аутентифицированные пользователи
        POST: /titles/{title_id}/reviews/{review_id}/comments/
    Получение комментария к отзыву: Доступно без токена
        GET: /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
    Частичное обновление комментария к отзыву:
    Автор комментария, модератор или админ
        PATCH: /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
    Удаление комментария к отзыву: Автор комментария, модератор или админ
        DELETE: /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self) -> QuerySet:
        """Возвращает комментарий."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Создаёт комментарий в БД."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
