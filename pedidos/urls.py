from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstadoPedidoGenericView, PedidoViewSet ,PedidoItemViewSet

router = DefaultRouter()
#router.register(r'tipos-de-estados-de-pedidos', viewset=EstadoPedidoViewSet, basename='tipos-de-estados-para-pedidos')
router.register(r'pedidos', PedidoViewSet, basename='pedidos')
router.register(r'items-de-pedidos', PedidoItemViewSet, basename='items-de-pedidos')



urlpatterns = [
    path('estados-pedido',EstadoPedidoGenericView.as_view(), name="estado-pedido-list"),
    path('', include(router.urls))
]