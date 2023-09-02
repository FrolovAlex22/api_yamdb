from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .permissions import IsAdminOrSuperuser
from .serializers import TitlesSerializer, GenreSerializer, CategorySerializer

from reviews.models import Category, Genre, Titles


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
    permission_classes = (AllowAny, )

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
    permission_classes = (AllowAny, )

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
    permission_classes = (AllowAny, )

    def get_permissions(self):
        if self.action == ('create' or 'destroy'):
            return (IsAdminOrSuperuser(),)
        return super().get_permissions()
