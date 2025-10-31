from rest_framework import serializers
from .models import Carrito, Orden, OrdenItem, EstadoPago
from django.contrib.auth.models import User
from productos.models import Producto

class CarritoSerializer(serializers.ModelSerializer):
    
    usuario_creador = serializers.PrimaryKeyRelatedField(
        default = serializers.CurrentUserDefault(),
        read_only = True
        )

    def create(self,data):
        request = self.context.get('request')
        data['usuario_creador'] = request.user
        return super().create(data)


    def validate(self, data):
        producto = data['producto']
        data['precio_unitario'] = producto.precio
        data['precio'] = data['cantidad']* data['precio_unitario']
        cantidad = data['cantidad']
        if cantidad > producto.stock:
            raise serializers.ValidationError(f"Stock insuficiente: Stock actual: {producto.stock}")
        return data
    
    class Meta:
        model = Carrito
        fields = ['cliente','producto','cantidad','precio_unitario','precio','usuario_creador']
        extra_kwargs = {
            'precio':{'read_only':True},
            'precio_unitario':{'read_only':True},
            'cliente': {'required':True}
        }


class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = '__all__'

class OrdenSerializer(serializers.ModelSerializer):
    ordenitems = OrdenItemSerializer(many=True, read_only = True, source='items') 
    class Meta:
        model = Orden
        fields = ['cliente','estado_pago','total','fecha','ordenitems','usuario_creador']
        extra_kwargs = {
            'usuario_creador': {'read_only':True}
        }


class EstadoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPago
        fields = ['nombre']
        extra_kwargs = {
            'nombre':{'required':True}
        }