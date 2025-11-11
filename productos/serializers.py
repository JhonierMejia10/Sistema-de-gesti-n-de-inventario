from rest_framework import serializers
from categorias.models import Categoria
from compras.models import Proveedor
from .models import TipoProducto,Marca, Producto, TipoAtributoProducto, AtributoProducto


class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = ['nombre']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['nombre']

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
        
    def validate_precio(self, validate_data):
        if validate_data < 0:
            raise serializers.ValidationError("El valor no puede ser menor a cero")
        return validate_data


class TipoAtrubutoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAtributoProducto
        fields = ['nombre']


class AtributoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoProducto
        fields = ['producto','tipo_atributo','valor']