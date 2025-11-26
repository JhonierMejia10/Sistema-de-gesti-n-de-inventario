from django.urls import path
from rest_framework import routers
from .views import PagoVentaViewSet, MedioPagoViewSet


router = routers.DefaultRouter()
router.register(r'pagos', PagoVentaViewSet, basename='pago')
router.register(r'medios-de-pago', MedioPagoViewSet, basename='medio-pago')

urlpatterns = router.urls