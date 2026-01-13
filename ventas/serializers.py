from rest_framework import serializers
from .models import TipoEntrega, Orden, OrdenItem
from django.contrib.auth.models import User
from productos.models import Producto

class TipoEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEntrega
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


