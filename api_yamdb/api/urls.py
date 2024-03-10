from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet
from api.views import CategoryViewSet

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
