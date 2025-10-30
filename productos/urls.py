from django.urls import path, include
from .views import ProductoViewSet, MarcaViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet, basename="Productos")
router.register(r'marcas', MarcaViewSet, basename='marcas')

urlpatterns = [
    path('', include(router.urls))
]