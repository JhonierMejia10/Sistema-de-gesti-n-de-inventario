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
    
    def validate_nombre(self, value):
        qs = Almacen.objects.filter(nombre__iexact=value)

        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists:
            raise serializers.ValidationError("Ya existe un estado con este nombre (independiente de mayúsculas/minúsculas).")
        return value
        
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ubicacion'] = UbicacionSerializer(instance.ubicacion).data
        return representation
    
    extra_kwargs = {
        'slug': {'read_only': True}
    }

    