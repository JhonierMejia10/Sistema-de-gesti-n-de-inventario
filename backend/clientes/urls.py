from django.urls import path, include
from .views import ClienteViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'clientes',ClienteViewSet, basename="cliente")

urlpatterns = [
    path('', include(router.urls))
]