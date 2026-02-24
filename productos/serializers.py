from rest_framework import serializers
from categorias.models import Categoria
from compras.models import Proveedor
from .models import TipoProducto, Marca, Producto, TipoAtributoProducto, AtributoProducto
from inventario.models import Stock
from almacenes.models import Almacen
from categorias.models import Categoria

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class CrearProductoSerializer(serializers.Serializer):
    """Serializer específico para crear nuevo producto"""
    nombre = serializers.CharField(required=True, allow_null=False)
    descripcion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    precio = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0 ,allow_null=False)
    foto = serializers.ImageField(required=False)
    categoria = serializers.PrimaryKeyRelatedField(
        queryset = Categoria.objects.all(), 
        required=True
    )
    marca = serializers.PrimaryKeyRelatedField(
        queryset = Marca.objects.all(), 
        required=False,
        allow_null=True
    )
    tipo_producto = serializers.PrimaryKeyRelatedField(
        queryset = TipoProducto.objects.all(), 
        required=True
    )
    nota = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=None)
    stock_inicial = serializers.IntegerField(min_value=0, required=True)
    almacen = serializers.PrimaryKeyRelatedField(
        queryset = Almacen.objects.all(),
        required = True
    )

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ['id','fecha_creacion']

class TipoAtrubutoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAtributoProducto
        fields = '__all__'

class AtributoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoProducto
        fields = '__all__'