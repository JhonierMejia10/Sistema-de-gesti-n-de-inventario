from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MedioPago, PagoVenta, PagoCompra
from .serializers import MedioPagoSerializer, PagoVentaSerializer, PagoCompraSerializer
from .services import PagoService
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class PagoVentaViewSet(viewsets.ModelViewSet):
    queryset = PagoVenta.objects.select_related('metodo_pago', 'orden').all()
    serializer_class = PagoVentaSerializer
    search_fields = ['id', 'orden__id', 'orden__cliente__nombre']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Sobrescribir create para usar el servicio
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            pago = PagoService.registrar_pago_venta(
                orden=serializer.validated_data['orden'],
                monto=serializer.validated_data['monto'],
                metodo_pago=serializer.validated_data['metodo_pago'],
                usuario=request.user,
                nota=serializer.validated_data.get('nota', '')
            )

            output_serializer = self.get_serializer(pago)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MedioPagoViewSet(viewsets.ModelViewSet):
    queryset = MedioPago.objects.all()
    serializer_class = MedioPagoSerializer
    search_fields = ['id', 'nombre']
    permission_classes = [IsAuthenticated]  

class PagoCompraViewSet(viewsets.ModelViewSet):
    queryset = PagoCompra.objects.select_related('metodo_pago', 'orden_compra').all()
    serializer_class = PagoCompraSerializer
    search_fields = ['id', 'orden_compra__id', 'orden_compra__proveedor__nombre']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Sobrescribir create para usar el servicio de compras
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            pago = PagoService.registrar_pago_compra(
                orden_compra=serializer.validated_data['orden_compra'],
                monto=serializer.validated_data['monto'],
                metodo_pago=serializer.validated_data['metodo_pago'],
                usuario=request.user,
                nota=serializer.validated_data.get('nota', '')
            )

            output_serializer = self.get_serializer(pago)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
