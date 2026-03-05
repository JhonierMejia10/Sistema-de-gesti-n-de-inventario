from rest_framework import serializers
from .models import  MedioPago, PagoVenta, PagoCompra

class MedioPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioPago
        fields = ['id', 'nombre', 'descripcion']

class PagoVentaSerializer(serializers.ModelSerializer):
    metodo_pago_nombre = serializers.CharField(source='metodo_pago.nombre', read_only=True)
    
    class Meta:
        model = PagoVenta
        fields = ['id', 'orden', 'metodo_pago', 'metodo_pago_nombre', 'fecha', 'monto', 'nota']

class PagoCompraSerializer(serializers.ModelSerializer):
    metodo_pago_nombre = serializers.CharField(source='metodo_pago.nombre', read_only=True)
    
    class Meta:
        model = PagoCompra
        fields = ['id', 'orden_compra', 'metodo_pago', 'metodo_pago_nombre', 'fecha', 'monto', 'nota']