from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import TipoEntregaSerializer ,OrdenSerializer, OrdenItemSerializer
from .models import TipoEntrega, Carrito, CarritoItem, Orden, OrdenItem
from .permissions import PermitirTodo, PermitirAdmin
from rest_framework.response import Response
from core.models import EstadoPago
from clientes.models import Cliente
from inventario.models import Almacen
from productos.models import Producto
from .services import OrdenVentaService
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from rest_framework.decorators import action
from django.db import transaction

# ViewSet para las reglas CRUD del modelo Tipos de entrega (Entrega en caja o pedido)
class TipoEntregaViewSet(viewsets.ModelViewSet):
    queryset = TipoEntrega.objects.all()
    serializer_class = TipoEntregaSerializer
    permission_classes = [PermitirTodo]


#Endpoint viewset para las ordenes
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [PermitirTodo]

        
#Endpoint viewset para los items de las ordenes
class OrdenItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrdenItem.objects.all()
    serializer_class = OrdenItemSerializer
    permission_classes = [PermitirAdmin]




