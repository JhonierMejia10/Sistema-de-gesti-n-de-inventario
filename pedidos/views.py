from .models import EstadoPedido, Pedido, PedidoItem
from .serializers import EstadoPedidoSerializer, PedidoSerializer, PedidoItemSerializer
from .permissions import PermitirTodo
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser

from rest_framework import viewsets
# Create your views here.

class EstadoPedidoGenericView(generics.ListAPIView):
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [IsAdminUser]

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class= PedidoSerializer
    permission_classes = [PermitirTodo]

class PedidoItemViewSet(viewsets.ModelViewSet):
    queryset = PedidoItem.objects.all()
    serializer_class = PedidoItemSerializer
    permission_classes = [PermitirTodo]
