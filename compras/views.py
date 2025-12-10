from rest_framework import viewsets
from rest_framework import status
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from rest_framework.response import Response

from .models import Proveedor, EstadoCompra, OrdenCompra, ItemOrdenCompra
from .serializers import ProveedorSerializer, EstadoCompraSerializer, OrdenCompraSerializer, ItemoOrdenCompraSerializer, CrearCompraSerializer, ActualizarCompraSerializer
from .permissions import PermitirTodo
from .services import CompraService

# Create your views here.

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    lookup_field = 'slug'
    permission_classes = [PermitirTodo]

class EstadoCompraViewSet(viewsets.ModelViewSet):
    queryset = EstadoCompra.objects.all()
    serializer_class = EstadoCompraSerializer
    permission_classes = [PermitirTodo]

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenCompraSerializer
    permission_classes = [PermitirTodo]

    def get_serializer_class(self):
        if self.action == 'create':
            return CrearCompraSerializer
        elif self.action in ['update', 'partial_update']:
            return ActualizarCompraSerializer
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
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = ActualizarCompraSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        # Extraer estado_compra e items por separado
        estado_compra = data.pop('estado_compra', None)
        items = data.pop('items', None)
        
        # Todo lo demás va en kwargs (solo los campos presentes)
        service_kwargs = data  # Aquí solo quedan ubicacion_entrega, proveedor, nota (si vinieron)
        
        try:
            orden_actualizada = CompraService.actualizar_compra_service(
                orden_compra_id=instance.id,
                estado_compra=estado_compra,
                items=items,
                usuario_modificador=request.user,
                **service_kwargs
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orden_serializer = OrdenCompraSerializer(orden_actualizada)
        return Response(orden_serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    

class ItemOrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = ItemOrdenCompra.objects.all()
    serializer_class = ItemoOrdenCompraSerializer
    permission_classes = [PermitirTodo]