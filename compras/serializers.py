from rest_framework import serializers
from .models import Proveedor, EstadoCompra, OrdenCompra, ItemOrdenCompra
from productos.models import Producto
from inventario.models import Almacen
from .services import CompraService


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

        extra_kwargs = {
            'nombre':{'required':True},
            'slug':{'read_only':True}
        }

class EstadoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCompra
        fields = '__all__'
        
        extra_kwargs = {
            'nombre':{'required':True}
        }

"""Serializers usados if action is not 'create'"""
class ItemOrdenCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrdenCompra
        fields = ["id", "producto", "cantidad", "precio_unitario"]


class OrdenCompraSerializer(serializers.ModelSerializer):
    items = ItemOrdenCompraSerializer(many=True, required=False)
    items_a_eliminar = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = OrdenCompra
        fields = "__all__"

    def update(self, instance, validated_data):
        usuario = self.context["request"].user
        return CompraService.actualizar_orden(instance, validated_data, usuario)

"""Serializers usados if action = 'create'"""
class ItemCompraSerializer(serializers.Serializer):
    producto = serializers.PrimaryKeyRelatedField(
        queryset = Producto.objects.all()
    )
    cantidad = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )

class CrearCompraSerializer(serializers.Serializer):
    ubicacion_entrega = serializers.PrimaryKeyRelatedField(
        queryset = Almacen.objects.all()
    )
    proveedor = serializers.PrimaryKeyRelatedField(
        queryset = Proveedor.objects.all()
    )
    estado_compra = serializers.PrimaryKeyRelatedField(
        queryset = EstadoCompra.objects.all()
    )
    items = ItemCompraSerializer(many=True)
    nota = serializers.CharField(required=False, allow_null=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Debes incluir al menos un producto.")
        return value
    
