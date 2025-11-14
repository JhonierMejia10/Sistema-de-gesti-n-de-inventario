from .models import Proveedor, EstadoCompra, OrdenCompra, ItemOrdenCompra
from .serializers import ProveedorSerializer, EstadoCompraSerializer, OrdenCompraSerializer, ItemoOrdenCompraSerializer
from .permissions import PermitirTodo
from rest_framework import viewsets

# Create your views here.

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [PermitirTodo]

class EstadoCompraViewSet(viewsets.ModelViewSet):
    queryset = EstadoCompra.objects.all()
    serializer_class = EstadoCompraSerializer
    permission_classes = [PermitirTodo]

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenCompraSerializer
    permission_classes = [PermitirTodo]


class ItemOrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = ItemOrdenCompra.objects.all()
    serializer_class = ItemoOrdenCompraSerializer
    permission_classes = [PermitirTodo]