from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import F
from .serializers import OrdenSerializer, OrdenItemSerializer, CrearOrdenVentaSerializer
from .models import Orden, OrdenItem
from rest_framework.response import Response
from .services import OrdenVentaService
from django.core.exceptions import ValidationError

from rest_framework.decorators import action

#Endpoint viewset para las ordenes
class OrdenVentaViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.select_related(
        'cliente', 'estado_pago', 'almacen'
    ).prefetch_related('items', 'items__producto').all()
    serializer_class = OrdenSerializer
    search_fields = ['id', 'cliente__nombre', 'cliente__nit']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        con_saldo = self.request.query_params.get('con_saldo')
        if con_saldo and con_saldo.lower() == 'true':
            queryset = queryset.filter(total_pagado__lt=F('total'))
        return queryset

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
                items=data["items"],
                cliente=data["cliente"],
                usuario_creador=request.user,
                tipo_entrega=data["tipo_entrega"],
                pago_inicial=data.get('pago_inicial', 0),
                metodo_pago=data.get('metodo_pago'),
                nota=data.get('nota'),
                direccion_envio=data.get('direccion_envio')
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




