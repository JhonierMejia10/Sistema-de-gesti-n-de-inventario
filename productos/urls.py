from django.urls import path, include
from .views import TipoProductoViewSet, MarcaViewSet ,ProductoViewSet
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'tipos-de-producto', TipoProductoViewSet, basename='tipos-de-producto')
router.register(r'marcas', MarcaViewSet, basename='marcas')
router.register(r'productos', ProductoViewSet, basename="Productos")


urlpatterns = [
    path('', include(router.urls))
]