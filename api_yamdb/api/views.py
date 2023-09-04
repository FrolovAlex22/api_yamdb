from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from django.db.models.query import QuerySet

from reviews.models import Review, Category, Genre, Titles
from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitlesSerializer,
    GenreSerializer,
    CategorySerializer
)
from .permissions import (
    IsAuthorModeratorAdminOrReadOnly,
    IsAdminOrSuperuser
)


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
        title = get_object_or_404(Titles, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Создаёт отзыв в БД."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
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


class TitlesViewSet(viewsets.ModelViewSet):
    """
    ViewSet служит для:
    Получение списка всех произведений.
    Получение информации о произведении.
    Добавление произведения.
    Частичное или полное обновление информации о произведении.
    Удаление произведения.
    """
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.action == (
                'create' or 'destroy' or 'partial_update' or 'update'
        ):
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()


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
    ViewSet GenreViewSet служит для:
    Получение списка всех жанров.
    Добавление жанра.
    Удаление жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.action == ('create' or 'destroy'):
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()


class CategoryViewSet(ListCreateDeleteViewSet):
    """
    ViewSet CategoryViewSet служит для:
    Получение списка всех категорий.
    Добавление категории.
    Удаление категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.action == ('create' or 'destroy'):
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()
