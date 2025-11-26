from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializers import TipoEntregaSerializer ,CarritoSerializer, OrdenSerializer, OrdenItemSerializer, AgregarCarritoSerializer
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

class CarritoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id is None:
            carritos = Carrito.objects.all()
            serializer = CarritoSerializer(carritos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                carrito = Carrito.objects.get(id=id)
                serializer = CarritoSerializer(carrito)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({'error':"Carrito no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = AgregarCarritoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        """Prueba usando un usuario de la bd como usuario registrado (No usar en producción)
        if request.user.is_authenticated:
            usuario = request.user
        else:
            # Usa un usuario de prueba (cámbialo por un ID que exista en tu BD)
            usuario = User.objects.get(id=1)
        """
        try:
            usuario = request.user
        except:
            return Response("Debe autenticarse para poder interactuar con esta acción.")

        #Cargar instancias desde los ids validos
        cliente_id = data.get("cliente_id")
        cliente = None
        if cliente_id is not None:
            cliente = Cliente.objects.filter(id=cliente_id).first()
        
        almacen = Almacen.objects.get(id=data["almacen_id"])
        producto = Producto.objects.get(id=data["producto_id"])

        try:
            item = OrdenVentaService.agregar_al_carrito(
                usuario_creador=usuario,
                cliente_id=cliente.id if cliente else None,
                almacen=almacen,
                producto=producto,
                cantidad=data["cantidad"],
                precio_unitario=data["precio_unitario"]
            )
        except Exception as e:
            return Response(
                {'error':str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"mensaje": "Producto agregado al carrito exitosamente",
            "carrito_item_id": item.id,
            "producto": item.producto.nombre,
            "cantidad_total_en_carrito": item.cantidad
            },
            status=status.HTTP_200_OK
        )
    


#Endpoint viewset para las ordenes
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [PermitirTodo]

    def get_queryset(self):
        cliente_id = self.request.query_params.get('cliente')
        if cliente_id:
            return Orden.objects.filter(cliente_id=cliente_id)
        
        if self.request.user.is_staff:
            return Orden.objects.all()
        
        return Orden.objects.none()

    @action(detail=False, methods=['post'])
    def crear_desde_carrito(self, request):
        """
        Endpoint que recibe la petición HTTP.
        Valida los datos y delega al servicio.
        """
        cliente_id = request.data.get('cliente_id')
        almacen_id = request.data.get('almacen_id')
        pago_inicial = request.data.get('pago_inicial') #El pago inicial es opcional
        
        #Validar que se haya seleccionado el almacen:
        if not almacen_id:
            return Response(
                {'error': 'El campo almacen no puede estar vacío.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            service = OrdenVentaService()

            orden = service.crear_orden_desde_carrito(
                cliente_id=cliente_id,
                usuario_creador=request.user,
                almacen_id=almacen_id,
                pago_inicial=pago_inicial
            )
            serializer = OrdenSerializer(orden)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#Endpoint viewset para los items de las ordenes
class OrdenItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrdenItem.objects.all()
    serializer_class = OrdenItemSerializer
    permission_classes = [PermitirAdmin]




