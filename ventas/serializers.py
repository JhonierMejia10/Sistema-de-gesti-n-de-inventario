from rest_framework import serializers
from .models import TipoEntrega, Orden, OrdenItem
from .services import OrdenVentaService
from django.contrib.auth.models import User
from productos.models import Producto
from almacenes.models import Almacen
from core.models import EstadoPago
from clientes.models import Cliente


class TipoEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEntrega
        fields = '__all__'

class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = '__all__'

class OrdenItemWriteSerializer(serializers.Serializer):
    producto = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all()
    )
    cantidad = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0
    )

class OrdenSerializer(serializers.ModelSerializer):
    items = OrdenItemWriteSerializer(many=True, required=False)
    class Meta:
        model = Orden
        fields = [
            'id',
            'cliente',
            'usuario_creador',
            'fecha',
            'estado_pago',
            'nota',
            'items',        
            'total'
        ]
        extra_kwargs = {
            'usuario_creador': {'read_only': True}
        }

    def update(self, instance, validated_data):
        usuario = self.context["request"].user
        return OrdenVentaService.actualizar_orden_venta(
            instance,
            validated_data,
            usuario
        )




"""Serializers usados en create"""
class ItemOrdenVentaSerializer(serializers.Serializer):
    producto = serializers.PrimaryKeyRelatedField(
        queryset = Producto.objects.all()
    )
    cantidad = serializers.IntegerField(min_value = 1)
    precio_unitario = serializers.DecimalField(
        max_digits=12,
        decimal_places=3,
        min_value=0.1
    )

class CrearOrdenVentaSerializer(serializers.Serializer):
    almacen = serializers.PrimaryKeyRelatedField(
        queryset = Almacen.objects.all()
    )
    estado_pago = serializers.PrimaryKeyRelatedField(
        queryset = EstadoPago.objects.all()
    )
    cliente = serializers.PrimaryKeyRelatedField(
        queryset = Cliente.objects.all()
    )
    tipo_entrega = serializers.PrimaryKeyRelatedField(
        queryset = TipoEntrega.objects.all()
    )
    items = ItemOrdenVentaSerializer(many=True)
    nota = serializers.CharField(required=False, allow_null=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Debes incluir al menos un producto")
        return value




