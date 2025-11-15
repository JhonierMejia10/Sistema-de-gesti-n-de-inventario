from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion','slug']
        read_only_fields = ['id','slug']

    def validate_nombre(self, value):
        qs = Categoria.objects.filter(nombre__iexact=value)

        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un estado con este nombre (independiente de mayúsculas/minúsculas).")  
        return value
    
    