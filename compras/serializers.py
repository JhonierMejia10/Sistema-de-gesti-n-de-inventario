from rest_framework import serializers
from .models import Proveedor, EstadoCompra, OrdenCompra, ItemOrdenCompra

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


    