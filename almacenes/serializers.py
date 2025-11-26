from rest_framework import serializers
from .models import Ubicacion, Almacen


class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'
    
class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = ['nombre','ubicacion','descripcion']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ubicacion'] = UbicacionSerializer(instance.ubicacion).data
        return representation
