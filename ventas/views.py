from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import TipoEntregaSerializer ,OrdenSerializer, OrdenItemSerializer, CrearOrdenVentaSerializer
from .models import TipoEntrega, Orden, OrdenItem
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
class OrdenVentaViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [PermitirTodo]

    def get_serializer_class(self):
        if self.action == 'create':
            return CrearOrdenVentaSerializer
        return OrdenSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = CrearOrdenVentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        

        
#Endpoint viewset para los items de las ordenes
class ItemOrdenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrdenItem.objects.all()
    serializer_class = OrdenItemSerializer
    permission_classes = [PermitirAdmin]




