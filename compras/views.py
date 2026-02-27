from rest_framework import viewsets
from rest_framework import status
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Proveedor, EstadoCompra, OrdenCompra, ItemOrdenCompra
from .serializers import ProveedorSerializer, EstadoCompraSerializer, OrdenCompraSerializer, ItemOrdenCompraSerializer, CrearCompraSerializer
from .permissions import PermitirTodo
from .services import CompraService

# Create your views here.

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

class EstadoCompraViewSet(viewsets.ModelViewSet):
    queryset = EstadoCompra.objects.all()
    serializer_class = EstadoCompraSerializer
    permission_classes = [IsAuthenticated]

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenCompraSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CrearCompraSerializer
        return OrdenCompraSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = CrearCompraSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            orden = CompraService.crear_compra_service(
                ubicacion_entrega=data['ubicacion_entrega'],
                proveedor=data['proveedor'],
                estado_compra=data['estado_compra'],
                items=data['items'],
                usuario_creador=request.user,
                nota=data.get('nota')
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orden_serializer = OrdenCompraSerializer(orden)
        return Response(orden_serializer.data, status=status.HTTP_201_CREATED)
    
class ItemOrdenCompraViewSet(viewsets.ModelViewSet):
    serializer_class = ItemOrdenCompraSerializer
    permission_classes = [IsAuthenticated]
    queryset = ItemOrdenCompra.objects.all()
    