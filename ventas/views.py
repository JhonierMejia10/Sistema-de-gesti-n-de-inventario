from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser
from .serializers import CarritoSerializer, OrdenSerializer, OrdenItemSerializer, EstadoPagoSerializer
from .models import Carrito, Orden, OrdenItem, EstadoPago
from movimientos.models import Movimiento, MovimientoItem
from rest_framework.response import Response


from rest_framework.decorators import action
from django.db import transaction

# Endpoint viewset para el carrito
class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
        
    def get_queryset(self):
        cliente_id = self.request.query_params.get('cliente')
        if cliente_id:
            return Carrito.objects.filter(cliente_id=cliente_id)
        return Carrito.objects.none()
    
    @action(detail=False, methods=['delete'])
    def vaciar(self, request):
        cliente_id = self.request.query_params.get('cliente')
        Carrito.objects.filter(cliente_id=cliente_id).delete()
        return Response({"message": "Carrito vaciado correctamente"})
    
    
#Endpoint viewset para las ordenes
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        cliente_id = self.request.query_params.get('cliente')
        if cliente_id:
            return Orden.objects.filter(cliente_id=cliente_id)
        
        if self.request.user.is_staff:
            return Orden.objects.all()
        
        return Orden.objects.none()

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def crear_desde_carrito(self, request):

        #Se obtiene el cliente asociado al carrito especificado en la consulta
        cliente_id = request.query_params.get('cliente')
        if not cliente_id:
            return Response(
                {"message": "Debe proporcionar un cliente válido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        #Se crea una variable donde se guarda la información del carrito del cliente proporcionado
        items_carrito = Carrito.objects.filter(cliente_id=cliente_id)
        if not items_carrito.exists():
            return Response(
                {"message": "No hay productos en el carrito"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = sum(item.precio for item in items_carrito)

        #Se crea un registro con la información del carrito que se guardará en la tabla Ordenes
        orden_data = {
            'cliente': cliente_id,
            'usuario_creador': request.user.id,
            'total': total,
            'estado_pago': 'Pendiente',
        }

        serializer = OrdenSerializer(data=orden_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        orden = serializer.save()

        for item in items_carrito:
            OrdenItem.objects.create(
                orden=orden,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.precio,
            )        

        items_carrito.delete()

        return Response(
            {
                "message": "Orden creada correctamente",
                "orden": OrdenSerializer(orden).data,
            },
            status=status.HTTP_201_CREATED,
        )


#Endpoint viewset para los items de las ordenes
class OrdenItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrdenItem.objects.all()
    serializer_class = OrdenItemSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    

#Endpoint viewset para los estados de pago
class EstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]