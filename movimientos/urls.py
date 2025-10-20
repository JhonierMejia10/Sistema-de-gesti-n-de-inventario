from .views import MovimientoInventarioViewSet
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'movimientos', MovimientoInventarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]