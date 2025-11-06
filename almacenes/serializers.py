from rest_framework import serializers
from .models import Sitio, Almacen


class SitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitio
        fields = '__all__'

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = ['nombre_almacen', 'sitio']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sitio'] = SitioSerializer(instance.sitio).data
        return representation
    
    extra_kwargs = {
        'slug': {'read_only': True}
    }

    