from rest_framework import serializers
from .models import Pago, EstadoPago, MedioPago

class EstadoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPago
        fields = ['nombre']
    
    def validate_nombre(self, validate_data):
        if self.instance:
            if EstadoPago.objects.filter(nombre=validate_data).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Este estado de pago ya existe.")
        else:
            if EstadoPago.objects.filter(nombre=validate_data).exists():
                raise serializers.ValidationError("Este estado de pago ya existe.")
        return validate_data


class MedioPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioPago
        fields = ['nombre']
    
    def validate_nombre(self, validate_data):
        if self.instance:
            if MedioPago.objects.filter(nombre=validate_data).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Este medio de pago ya existe.")
        else:
            if MedioPago.objects.filter(nombre=validate_data).exists():
                raise serializers.ValidationError("Este medio de pago ya existe.")
        return validate_data



class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['orden','estado_pago','fecha','monto']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['estado_pago'] = EstadoPagoSerializer(instance.estado_pago).data
        representation['metodo_pago'] = MedioPagoSerializer(instance.metodo_pago).data
        return representation
