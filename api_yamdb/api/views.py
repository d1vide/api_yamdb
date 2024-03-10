from rest_framework import mixins
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Review, Title
from .permissons import AuthorAdminModeratorOrReadOnly, AdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class ListCreateDestroyViewSet(mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly, )

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs.get('pk'))


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (AdminOrReadOnly, )

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs.get('pk'))


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly, )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if partial:
            instance = self.get_object()
            serializer = self.get_serializer(instance,
                                             data=request.data,
                                             partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(data={"detail": "Method \"PUT\" not allowed."},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
