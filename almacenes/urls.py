from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SitioViewSet, AlmacenViewSet


router = DefaultRouter()
router.register(r'sitios', SitioViewSet, basename='sitios')
router.register(r'almacenes', AlmacenViewSet, basename='almacenes')

urlpatterns = router.urls