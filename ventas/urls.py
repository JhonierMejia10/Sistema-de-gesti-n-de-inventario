from django.urls import path, include
from rest_framework import routers
from .views import TipoEntregaViewSet, OrdenViewSet, OrdenItemViewSet, CarritoAPIView

router = routers.DefaultRouter()
router.register(r'tipos-de-entrega', TipoEntregaViewSet, basename='tipos-de-entrega')
router.register(r'ordenes-de-venta', OrdenViewSet, basename='ordenes-de-venta'),
router.register(r'orden-items', OrdenItemViewSet, basename='orden-items')

urlpatterns = [
    path('', include(router.urls)),
    path('carrito/', CarritoAPIView.as_view()),
    path('carrito/<int:id>', CarritoAPIView.as_view()),
]