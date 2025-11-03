from rest_framework import serializers
from .models import Pago, EstadoPago, MedioPago


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fieds = ['orden','estado_pago','fecha','monto']
    

class EstadoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPago
        fields = ['nombre']

class MedioPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioPago
        fields = ['nombre']