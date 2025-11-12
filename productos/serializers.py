from rest_framework import serializers
from categorias.models import Categoria
from compras.models import Proveedor
from .models import TipoProducto,Marca, Producto, TipoAtributoProducto, AtributoProducto
from inventario.models import Stock
from almacenes.models import Almacen

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = ['nombre']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['nombre']

class StockInicialSerializer(serializers.Serializer):
    """Serializer específico para crear stock inicial con productos"""
    almacen = serializers.PrimaryKeyRelatedField(
        queryset = Almacen.objects.all()
    )
    cantidad_en_mano = serializers.IntegerField(min_value=0)

class ProductoSerializer(serializers.ModelSerializer):
    stock_inicial = StockInicialSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','tipo_producto','categoria','marca','foto','nota','stock_inicial']
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
    
    def create(self, validate_data):
        stock_data = validate_data.pop('stock_inicial', [])
        producto = Producto.objects.create(**validate_data)
        
        #Crear registros de stock:
        #**stock_item es la instancia completa
        for stock_item in stock_data:
            Stock.objects.create(
                producto=producto,
                **stock_item
            )
        return producto
        
class TipoAtrubutoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAtributoProducto
        fields = ['nombre']


class AtributoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoProducto
        fields = ['producto','tipo_atributo','valor']