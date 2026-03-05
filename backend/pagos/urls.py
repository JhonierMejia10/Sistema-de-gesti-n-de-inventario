from django.urls import path
from rest_framework import routers
from .views import MedioPagoViewSet, PagoVentaViewSet, PagoCompraViewSet


router = routers.DefaultRouter()
router.register(r'pagos-de-compras', PagoCompraViewSet, basename='pagos de compras')
router.register(r'medios-de-pago', MedioPagoViewSet, basename='medio-pago')
router.register(r'pagos-de-ventas', PagoVentaViewSet, basename='pagos de ventas')

urlpatterns = router.urls