from .views import StockViewSet, MovimientoViewSetOnlyView
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'movimientos', MovimientoViewSetOnlyView, basename='movimientos')
router.register(r'stocks', StockViewSet, basename='stocks')

urlpatterns = [
    path('', include(router.urls)),
]