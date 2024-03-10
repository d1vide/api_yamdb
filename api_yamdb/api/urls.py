from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       TitleViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
