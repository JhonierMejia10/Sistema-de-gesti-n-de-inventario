from django.urls import path, include
from .views import ClienteViewSet, TipoClienteViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'clientes',ClienteViewSet, basename="cliente")
router.register(r'tipos-clientes',TipoClienteViewSet, basename="tipocliente")

urlpatterns = [
    path('', include(router.urls))
]