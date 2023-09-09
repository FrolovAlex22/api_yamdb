from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_201_CREATED,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Review, Category, Genre, Titles
from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitlesSerializer,
    GenreSerializer,
    CategorySerializer,
    TitlesGetSerializer
)
from .permissions import (
    IsAuthorModeratorAdminOrReadOnly,
    IsAdminOrSuperuser,
    IsAuthenticated,
    IsAdmin
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

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre','name', 'year')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return self.serializer_class

    # def patch(self, request, pk):
    #     if not request.user.is_authenticated:
    #         return Response('Необходимо авторизоваться', status=HTTP_401_UNAUTHORIZED)
    #     title_obj = get_object_or_404(Titles, pk=pk)
    #     serializer = TitlesSerializer(title_obj, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=HTTP_201_CREATED)
    #     return Response("wrong parameters", status=HTTP_404_NOT_FOUND)

    # def update(self, request, pk, partial):
    #     title = get_object_or_404(Titles, pk=pk)
    #     data = request.data
    #     category = data.get('category')
    #     category_obj = get_object_or_404(Category,slug = category)
    #     genre = data.get('genre')
    #     genre_obj = get_object_or_404(Genre,slug = genre)
    #     name = data.get('name')
    #     if len(name) > 256:
    #         return Response('Необходимо авторизоваться', HTTP_404_NOT_FOUND)

    #     title.category = data.get(category_obj, title.category)
    #     title.genre = data.get(genre_obj, title.genre)
    #     title.name = data.get('name', title.name)
    #     title.year = data.get('year', title.year)

    #     title.save()
    #     serializer = TitlesSerializer(title)
    #     if not request.user.is_authenticated:
    #         return Response('Необходимо авторизоваться', HTTP_401_UNAUTHORIZED)
    #     return Response(serializer.data, status=HTTP_200_OK)


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Набор mixins для GenreViewSet, CategoryViewSet."""
    pass


class GenreViewSet(ListCreateDeleteViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
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
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()

