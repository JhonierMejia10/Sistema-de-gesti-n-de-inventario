from rest_framework import routers
from .views import EstadoPagoViewSet

router = routers.DefaultRouter()
router.register(r'estados-de-pago', EstadoPagoViewSet)

urlpatterns = router.urls