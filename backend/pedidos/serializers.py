from rest_framework import serializers
from .models import Pedido



class PedidoSerializer(serializers.ModelSerializer):
    """Serializer de lectura con datos enriquecidos de la orden asociada"""
    estado_nombre = serializers.CharField(source='get_estado_display', read_only=True)
    orden_id = serializers.IntegerField(source='orden.id', read_only=True)
    cliente_nombre = serializers.CharField(source='orden.cliente.nombre', read_only=True, default='General')
    orden_total = serializers.DecimalField(source='orden.total', max_digits=12, decimal_places=2, read_only=True)
    orden_fecha = serializers.DateField(source='orden.fecha', read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'fecha_creacion', 'direccion_envio', 'observaciones',
            'orden', 'estado',
            # Campos enriquecidos (solo lectura)
            'estado_nombre', 'orden_id', 'cliente_nombre', 'orden_total', 'orden_fecha',
        ]
        read_only_fields = ['orden', 'fecha_creacion']


class ActualizarPedidoSerializer(serializers.Serializer):
    """Solo permite actualizar el estado logístico y observaciones"""
    estado = serializers.ChoiceField(
        choices=Pedido.EstadoPedidoChoices.choices
    )
    observaciones = serializers.CharField(required=False, allow_null=True, allow_blank=True)