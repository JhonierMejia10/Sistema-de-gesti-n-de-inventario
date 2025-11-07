from rest_framework import serializers
from .models import Ubicacion, Almacen


class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'
    

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = '__all__'
    
    def validate_nombre(self, validate_data):
        
        if self.instance:
            if Almacen.objects.filter(nombre=validate_data).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Ya existe un almacen con este nombre.")
        
        else:
            if Almacen.objects.filter(nombre=validate_data).exists():
                raise serializers.ValidationError("Ya existe un almacen con este nombre.")
        return validate_data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sitio'] = UbicacionSerializer(instance.sitio).data
        return representation
    
    extra_kwargs = {
        'slug': {'read_only': True}
    }

    