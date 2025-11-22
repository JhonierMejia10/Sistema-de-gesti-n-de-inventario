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
        fields = ['nombre']

class CrearProductoSerializer(serializers.Serializer):
    """Serializer específico para crear nuevo producto"""
    nombre = serializers.CharField(required=True, allow_null=False)
    descripcion = serializers.CharField(required=False)
    precio = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0 ,allow_null=False)
    foto = serializers.ImageField(required=False)
    categoria = serializers.PrimaryKeyRelatedField(
        queryset = Categoria.objects.all()
    )
    marca = serializers.PrimaryKeyRelatedField(
        queryset = Marca.objects.all()
    )
    tipo_producto = serializers.PrimaryKeyRelatedField(
        queryset = TipoProducto.objects.all()
    )
    nota = serializers.CharField(required=False, allow_null=True, max_length=None)
    stock_inicial = serializers.IntegerField(min_value=0, required=True)
    almacen = serializers.PrimaryKeyRelatedField(
        queryset = Almacen.objects.all(),
        required = True
    )

    def validate(self, value):
        qs = Producto.objects.filter(nombre__iexact=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un producto con este nombre.")

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','tipo_producto','categoria','marca','foto','nota']
        read_only_fields = ['id','fecha_creacion']

        extra_kwargs = {
            'nombre':{'required':True},
            'precio':{'required':True},
            'categoria':{'required':True}
        }

class TipoAtrubutoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAtributoProducto
        fields = ['nombre']


class AtributoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoProducto
        fields = ['producto','tipo_atributo','valor']