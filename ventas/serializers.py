from rest_framework import serializers
from .models import TipoEntrega, Carrito, Orden, OrdenItem
from django.contrib.auth.models import User
from productos.models import Producto

class TipoEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEntrega
        fields = '__all__'

class AgregarCarritoSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField(required=False, allow_null=True)
    almacen_id = serializers.IntegerField(required=True)
    producto_id = serializers.IntegerField(required=True)
    cantidad = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(max_digits=12, decimal_places=2)

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'

class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = '__all__'

class OrdenSerializer(serializers.ModelSerializer):
    ordenitems = OrdenItemSerializer(many=True, read_only = True, source='items') 
    class Meta:
        model = Orden
        fields = ['cliente','usuario_creador','fecha','ordenitems','total']
        extra_kwargs = {
            'usuario_creador': {'read_only':True}
        }


