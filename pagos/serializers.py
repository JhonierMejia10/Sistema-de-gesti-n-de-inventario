from rest_framework import serializers
from .models import  MedioPago, PagoVenta, PagoCompra

class MedioPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioPago
        fields = ['nombre','descripcion']

class PagoVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoVenta
        fields = ['id', 'orden', 'metodo_pago', 'fecha', 'monto', 'nota']

class PagoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoCompra
        fields = ['id', 'orden_compra', 'metodo_pago', 'fecha', 'monto', 'nota']