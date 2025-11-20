from rest_framework import serializers
from .models import Stock, Movimiento, TipoMovimiento
from django.contrib.auth.models import User



class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

        extra_kwargs = {
            'producto':{'required':True},
            'almacen':{'required':True},
            'cantidad_en_mano':{'required':True}
        }

class TipoMovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoMovimiento
        fields = '__all__'

        extra_kwargs = {
            'nombre':{'required':True}
        }
    
    def validate_nombre(self, validate_data):
        if self.instance:
            if TipoMovimiento.objects.filter(nombre=validate_data).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Este tipo de movimiento ya existe.")
        else:
            if TipoMovimiento.objects.filter(nombre=validate_data).exists():
                raise serializers.ValidationError("Este tipo de movimiento ya existe.")
        return validate_data
    

class MovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movimiento
        fields = ['tipo_movimiento','fecha_creacion','usuario','nota']

        extra_kwargs = {
            'fecha':{'read_only':True},
            'usuario':{'read_only':True}
        }


