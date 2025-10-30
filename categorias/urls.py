from django.urls import path, include
from .views import CategoriaViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categorias',CategoriaViewSet, basename="categoria")

urlpatterns = [
    path('', include(router.urls))
]