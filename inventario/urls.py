from .views import StockViewSet, TipoMovimientoViewSet, MovimientoViewSet
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'movimientos', MovimientoViewSet, basename='movimientos')
router.register(r'tipos-de-movimiento', TipoMovimientoViewSet, basename='tipos-movimientos')
router.register(r'stocks', StockViewSet, basename='stocks')

urlpatterns = [
    path('', include(router.urls)),
]