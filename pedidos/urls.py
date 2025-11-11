from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EstadoPedidoViewSet, PedidoViewSet ,PedidoItemViewSet

router = DefaultRouter()
router.register(r'tipos-de-estados-de-pedidos', viewset=EstadoPedidoViewSet, basename='tipos-de-estados-para-pedidos')
router.register(r'pedidos', viewset=PedidoViewSet, basename='pedidos')
router.register(r'items-de-pedidos', viewset=PedidoItemViewSet, basename='items-de-pedidos')

urlpatterns = router.urls