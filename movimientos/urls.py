from .views import MovimientoViewSet, MovimientoItemViewSet
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'movimientos', MovimientoViewSet)
router.register(r'movimiento-items', MovimientoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]