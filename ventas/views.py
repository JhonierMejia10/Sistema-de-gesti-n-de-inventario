from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import TipoEntregaSerializer ,OrdenSerializer, OrdenItemSerializer, CrearOrdenVentaSerializer
from .models import TipoEntrega, Orden, OrdenItem
from .permissions import PermitirTodo, PermitirAdmin
from rest_framework.response import Response
from .services import OrdenVentaService
from django.core.exceptions import ValidationError

from rest_framework.decorators import action

# ViewSet para las reglas CRUD del modelo Tipos de entrega (Entrega en caja o pedido)
class TipoEntregaViewSet(viewsets.ModelViewSet):
    queryset = TipoEntrega.objects.all()
    serializer_class = TipoEntregaSerializer
    permission_classes = [IsAuthenticated]

#Endpoint viewset para las ordenes
class OrdenVentaViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CrearOrdenVentaSerializer
        return OrdenSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = CrearOrdenVentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            ordenVenta = OrdenVentaService.crear_orden_venta_service(
                almacen=data["almacen"],
                estado_pago=data["estado_pago"],
                items=data["items"],
                cliente=data["cliente"],
                usuario_creador=request.user,
                tipo_entrega=data["tipo_entrega"],
                nota=data.get('nota')
            )
        except ValidationError as e:
            return Response(
                {'error':str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        ordenVenta_serializer = OrdenSerializer(ordenVenta)
        return Response(ordenVenta_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # partial=True permite PATCH (campos opcionales), partial=False obliga PUT
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Usamos el mismo serializer de creación para validar la estructura de entrada
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        # En caso de PATCH, recuperamos los valores actuales si no vienen en el request
        almacen = data.get('almacen', instance.almacen)
        estado_pago = data.get('estado_pago', instance.estado_pago)
        cliente = data.get('cliente', instance.cliente)
        tipo_entrega = data.get('tipo_entrega', instance.tipo_entrega)
        nota = data.get('nota', instance.nota)
        items = data.get('items', None)
        
        if items is None:
            # Si en un PATCH no enviaron items, no actualizamos esa parte.
            # En un PUT normal 'items' es requerido por el serializer.
            # Para este diseño, forzamos requerir los items para poder calcular todo
            return Response(
                {'error': 'Se requiere proporcionar los items de la orden para actualizarla.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            ordenActualizada = OrdenVentaService.actualizar_orden_venta_service(
                orden_id=instance.id,
                almacen=almacen,
                estado_pago=estado_pago,
                cliente=cliente,
                usuario_modificador=request.user,
                tipo_entrega=tipo_entrega,
                items=items,
                nota=nota
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        orden_serializer = OrdenSerializer(ordenActualizada)
        return Response(orden_serializer.data, status=status.HTTP_200_OK)
        
 
#Endpoint viewset para los items de las ordenes
class ItemOrdenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrdenItem.objects.all()
    serializer_class = OrdenItemSerializer
    permission_classes = [IsAuthenticated]




