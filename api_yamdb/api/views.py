from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import CategorySerializer
from reviews.models import Category


class ListCreateDestroyViewSet(mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs.get('pk'))
