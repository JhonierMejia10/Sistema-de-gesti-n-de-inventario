from rest_framework import serializers
from .models import Cliente, TipoCliente


class TipoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCliente
        fields = ['nombre','descripcion']

        extra_kwargs = {
            'nombre': {'required':True},
            'id':{'read_only':True}
        }
    
    def validate_nombre(self, value):
        qs = TipoCliente.objects.filter(nombre__iexact=value)
        
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un tipo de cliente con este nombre.")
        return value


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['id']

        extra_kwargs = {
            'nombre': {'required':True}
        }
    

