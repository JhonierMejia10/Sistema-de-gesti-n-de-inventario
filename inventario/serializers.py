from rest_framework import serializers
from .models import Stock, Movimiento, TipoMovimiento
from django.contrib.auth.models import User

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class TipoMovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoMovimiento
        fields = '__all__'
    
class MovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movimiento
        fields = ['tipo_movimiento','fecha_creacion','usuario','nota']

        extra_kwargs = {
            'fecha_creacion':{'read_only':True},
            'usuario':{'read_only':True}
        }


