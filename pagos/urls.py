from django.urls import path
from rest_framework import routers
from .views import PagoViewSet, MedioPagoViewSet


router = routers.DefaultRouter()
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'medios-de-pago', MedioPagoViewSet, basename='medio-pago')

urlpatterns = router.urls