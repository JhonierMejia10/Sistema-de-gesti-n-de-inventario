from django.urls import path, include
from rest_framework import routers
from .views import CarritoViewSet, OrdenViewSet, OrdenItemViewSet

router = routers.DefaultRouter()
router.register(r'carrito', CarritoViewSet, basename='carrito')
router.register(r'ordenes', OrdenViewSet, basename='ordenes'),
router.register(r'orden-items', OrdenItemViewSet, basename='orden-items'),

urlpatterns = [
    path('', include(router.urls)),
]