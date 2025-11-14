from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UbicacionViewSet, AlmacenViewSet


router = DefaultRouter()
router.register(r'ubicaciones', UbicacionViewSet, basename='ubicaciones')
router.register(r'almacenes', AlmacenViewSet, basename='almacenes')

urlpatterns = router.urls