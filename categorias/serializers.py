from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']

        extra_kwargs = {
            'nombre':{'required': True, 'allow_blank':False}
        }

    def validate_nombre(self,validate_data):
        if Categoria.objects.filter(nombre=validate_data)
            raise serializers.ValidationError("Ya existe una categoría con este nombre.")
        return validate_data
    
    