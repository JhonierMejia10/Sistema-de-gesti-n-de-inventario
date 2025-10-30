from django.urls import path, include
from .views import ProductoViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet, basename="Productos")

urlpatterns = [
    path('', include(router.urls))
]