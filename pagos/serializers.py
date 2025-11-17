from rest_framework import serializers
from .models import  MedioPago, PagoVenta, PagoCompra

class MedioPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioPago
        fields = ['nombre','descripcion']
    
    def validate_nombre(self, value):
        qs = MedioPago.objects.filter(nombre__iexact=value)

        if self.instace:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Este medio de pago ya existe.")
        return value

class PagoVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoVenta
        fields = ['orden','metodo_pago','fecha','monto']
        read_only = ['orden']
    