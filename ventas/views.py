from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import CarritoSerializer, OrdenSerializer, OrdenItemSerializer
from .models import Carrito, Orden, OrdenItem
from rest_framework.response import Response

from rest_framework.decorators import action
from django.db import transaction

# Create your views here.

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
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cliente_id = self.request.query_params.get('cliente')
        cantidad_productos = Carrito.objects.filter(cliente_id = cliente_id).count()
        if cantidad_productos == 0:
            return Response({"message":"No hay productos en el carrito"})

        data = request.data.copy()
        total = self.get_total_price(cliente_id)
        data['usuario_creador'] = self.request.user.id
        data['total'] = total
        data['cliente'] = cliente_id
        data['estado_pago'] = 'Pendiente'
        Orden_Serializer = OrdenSerializer(data=data)

        if Orden_Serializer.is_valid():
            orden = Orden_Serializer.save()

            items = Carrito.objects.filter(cliente_id=cliente_id).all()

            for item in items:
                ordenitem = OrdenItem(
                    orden = orden,
                    producto = item.producto,
                    precio = item.precio,
                    cantidad = item.cantidad
                )
                ordenitem.save()
            
            Carrito.objects.filter(cliente_id=cliente_id).delete()

            result = Orden_Serializer.data.copy()
            result['total'] = total
            return Response(result)
        
        return Response(Orden_Serializer.errors, status=400)
        
    def get_total_price(self, cliente_id):
        total = 0
        items = Carrito.objects.filter(cliente_id=cliente_id).all()
        for item in items:
            total += item.precio 
        return total