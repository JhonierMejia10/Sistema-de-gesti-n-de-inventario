from rest_framework import viewsets
from rest_framework import status
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from django.db.models import F
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Proveedor, OrdenCompra, ItemOrdenCompra
from .serializers import ProveedorSerializer, OrdenCompraSerializer, ItemOrdenCompraSerializer, CrearCompraSerializer, ActualizarCompraSerializer
from .services import CompraService

# Create your views here.

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    search_fields = ['id', 'nombre', 'nit', 'correo']
    permission_classes = [IsAuthenticated]

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.select_related(
        'proveedor', 'estado_pago', 'ubicacion_entrega'
    ).prefetch_related('items', 'items__producto').all()
    serializer_class = OrdenCompraSerializer
    search_fields = ['id', 'proveedor__nombre', 'proveedor__nit']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        con_saldo = self.request.query_params.get('con_saldo')
        if con_saldo and con_saldo.lower() == 'true':
            queryset = queryset.filter(total_pagado__lt=F('total'))
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CrearCompraSerializer
        if self.action in ['update', 'partial_update']:
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
                fecha_esperada=data.get('fecha_esperada'),
                pago_inicial=data.get('pago_inicial', 0),
                metodo_pago=data.get('metodo_pago'),
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
        return self._handle_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._handle_update(request, *args, **kwargs)

    def _handle_update(self, request, *args, **kwargs):
        serializer = ActualizarCompraSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            orden = CompraService.actualizar_orden_compra_service(
                orden_id=kwargs['pk'],
                estado_compra=data['estado_compra'],
                usuario=request.user,
                nota=data.get('nota')
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        orden_serializer = OrdenCompraSerializer(orden)
        return Response(orden_serializer.data, status=status.HTTP_200_OK)

class ItemOrdenCompraViewSet(viewsets.ModelViewSet):
    serializer_class = ItemOrdenCompraSerializer
    permission_classes = [IsAuthenticated]
    queryset = ItemOrdenCompra.objects.all()
