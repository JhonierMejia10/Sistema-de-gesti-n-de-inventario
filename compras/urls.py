from django.urls import path, include
from rest_framework import routers
from .views import ProveedorViewSet, EstadoCompraViewSet, OrdenCompraViewSet, ItemOrdenCompraViewSet


router = routers.DefaultRouter()
router.register(r'proveedores', ProveedorViewSet, basename="Proveedores")
router.register(r'estados-de-compra', EstadoCompraViewSet, basename="estados-de-compra")
router.register(r'ordenes-de-compra', OrdenCompraViewSet, basename="odenes-de-compra")
router.register(r'items-de-ordenes-de-compra', ItemOrdenCompraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]