from .views import StockViewSet, TipoMovimientoViewSet, MovimientoViewSet, MovimientoItemViewSet
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'movimientos', MovimientoViewSet, basename='movimientos')
router.register(r'movimiento-items', MovimientoItemViewSet, basename='movimiento-items')
router.register(r'tipos-movimientos', TipoMovimientoViewSet, basename='tipos-movimientos')
router.register(r'stocks', StockViewSet, basename='stocks')

urlpatterns = [
    path('', include(router.urls)),
]