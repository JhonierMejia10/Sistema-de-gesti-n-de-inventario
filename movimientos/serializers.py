from rest_framework import serializers
from .models import Movimiento, MovimientoItem, TipoMovimiento
from django.contrib.auth.models import User

class MovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movimiento
        fields = ['tipo_movimiento','fecha_creacion','usuario','nota']

        extra_kwargs = {
            'fecha':{'read_only':True},
            'usuario':{'read_only':True}
        }


class MovimientoItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MovimientoItem
        fields = '__all__'
        
        extra_kwargs = {
            'movimiento':{'read_only':True}
        }


class TipoMovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoMovimiento
        fields = '__all__'

        extra_kwargs = {
            'nombre':{'required':True}
        }
    
    