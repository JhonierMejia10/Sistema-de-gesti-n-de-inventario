from rest_framework import serializers
from .models import Proveedor, EstadoCompra, OrdenCompra, ItemOrdenCompra
from productos.models import Producto
from almacenes.models import Almacen

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


class ItemOrdenCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrdenCompra
        fields = ["orden_compra","id", "producto", "cantidad", "precio_unitario"]
        read_only_fields = ['orden_compra']
    

class OrdenCompraSerializer(serializers.ModelSerializer):
    items = ItemOrdenCompraSerializer(many=True, required=False)
    class Meta:
        model = OrdenCompra
        fields = "__all__"

"""Serializers usados para la creación de una orden de comora"""
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

    
