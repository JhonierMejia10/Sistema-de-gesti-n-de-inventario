from rest_framework import serializers
from .models import EstadoPago

class EstadoPagoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EstadoPago
        fields = ['nombre','descripcion']
        only_read_fields = ['id']
    
    def validate_nombre(self, value):
        qs = EstadoPago.objects.filter(nombre__iexact=value)

        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un estado de pago con este nombre.")
        return value