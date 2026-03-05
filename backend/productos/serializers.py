from rest_framework import serializers
from categorias.models import Categoria
from .models import Marca, Producto
from inventario.models import Stock
from almacenes.models import Almacen

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
    tipo_producto = serializers.ChoiceField(
        choices=[('Bienes', 'Bienes'), ('Servicios', 'Servicios')],
        required=True
    )
    nota = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=None)
    stock_inicial = serializers.IntegerField(min_value=0, required=True)
    almacen = serializers.PrimaryKeyRelatedField(
        queryset = Almacen.objects.all(),
        required = True
    )

class StockPorAlmacenSerializer(serializers.Serializer):
    almacen_id = serializers.IntegerField(source='almacen.id')
    almacen_nombre = serializers.CharField(source='almacen.nombre')
    cantidad = serializers.IntegerField(source='cantidad_en_mano')

class ProductoSerializer(serializers.ModelSerializer):
    stock_por_almacen = serializers.SerializerMethodField()
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')

    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ['id','fecha_creacion']

    def get_stock_por_almacen(self, obj):
        # Si el queryset viene con prefetch, usa los datos precargados
        stocks = obj.stock_set.all()
        return StockPorAlmacenSerializer(stocks, many=True).data
