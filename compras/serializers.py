from rest_framework import serializers
from .models import Proveedor, EstadoCompra, OrdenCompra, ItemOrdenCompra
from productos.models import Producto
from inventario.models import Almacen


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
class OrdenCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenCompra
        fields = '__all__'

        extra_kwargs = {
            'fecha_orden':{'read_only':True},
            'usuario_creador':{'read_only':True}
        }

class ItemoOrdenCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrdenCompra
        fields = ['producto','cantidad','precio_unitario','orden_compra']


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
    

class ActualizarCompraSerializer(serializers.Serializer):
    ubicacion_entrega = serializers.PrimaryKeyRelatedField(
        queryset=Almacen.objects.all(),
        required=False
    )
    proveedor = serializers.PrimaryKeyRelatedField(
        queryset=Proveedor.objects.all(),
        required=False
    )
    estado_compra = serializers.PrimaryKeyRelatedField(
        queryset=EstadoCompra.objects.all(),
        required=False
    )
    items = ItemCompraSerializer(many=True, required=False)
    nota = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_items(self, value):
        if value is not None and len(value) == 0:
            raise serializers.ValidationError("Si incluyes items, debe haber al menos uno.")
        return value