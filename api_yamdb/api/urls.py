from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
