from django.urls import path, include
from rest_framework import routers
from .views import TipoEntregaViewSet, OrdenVentaViewSet, ItemOrdenViewSet

router = routers.DefaultRouter()
router.register(r'tipos-de-entrega', TipoEntregaViewSet, basename='tipos-de-entrega')
router.register(r'ordenes-de-venta', OrdenVentaViewSet, basename='ordenes-de-venta'),
router.register(r'orden-items', ItemOrdenViewSet, basename='orden-items')

urlpatterns = [
    path('', include(router.urls)),
]