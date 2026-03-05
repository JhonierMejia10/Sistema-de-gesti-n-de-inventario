from django.urls import path, include
from .views import MarcaViewSet ,ProductoViewSet
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'marcas', MarcaViewSet, basename='marcas')
router.register(r'productos', ProductoViewSet, basename="Productos")


urlpatterns = [
    path('', include(router.urls))
]