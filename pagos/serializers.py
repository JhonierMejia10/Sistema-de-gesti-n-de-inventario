from rest_framework import serializers
from .models import  MedioPago, PagoVenta, PagoCompra

class MedioPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioPago
        fields = ['nombre','descripcion']

class PagoVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoVenta
        fields = ['orden','metodo_pago','fecha','monto']
        read_only = ['orden']
    