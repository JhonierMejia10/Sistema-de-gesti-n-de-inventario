from django.urls import path, include
from rest_framework import routers
from .views import CarritoViewSet, OrdenViewSet, OrdenItemView, EstadoPagoViewSet

router = routers.DefaultRouter()
router.register(r'carrito', CarritoViewSet, basename='carrito')
router.register(r'ordenes', OrdenViewSet, basename='ordenes'),
router.register(r'orden-items', OrdenItemView, basename='orden-items'),
router.register(r'estado-pagos', OrdenViewSet, basename='estado-pagos')

urlpatterns = [
    path('', include(router.urls)),
]