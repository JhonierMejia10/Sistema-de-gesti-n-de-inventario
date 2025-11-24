from rest_framework import serializers
from .models import EstadoPago

class EstadoPagoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EstadoPago
        fields = ['nombre','descripcion']
        only_read_fields = ['id']
