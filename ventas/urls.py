from django.urls import path, include
from rest_framework import routers
from .views import CarritoViewSet

router = routers.DefaultRouter()
router.register(r'carrito', CarritoViewSet, basename='carrito')

urlpatterns = [
    path('', include(router.urls))
]