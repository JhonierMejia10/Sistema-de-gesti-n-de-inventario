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
    
    def validate_nombre(self, validate_data):
        if self.instance:
            if TipoCliente.objects.filter(nombre=validate_data).exclude(id=self.instance.id).exists():
                return serializers.ValidationError("Ya existe un tipo de cliente con este error")
        else:
            if TipoCliente.objects.filter(nombre=validate_data):
                return serializers.ValidationError("Ya existe un tipo de cliente con este error")
        return validate_data


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['id']

        extra_kwargs = {
            'nombre': {'required':True}
        }
    
    def validate_nit(self, validate_data):

        if self.instance:
            if Cliente.objects.filter(nit=validate_data).exclude(id=self.instance.id).exists():
                return serializers.ValidationError("Este cliente ya existe")
        else:
            if Cliente.objects.filter(nit=validate_data).exists():
                return serializers.ValidationError("Este cliente ya existe")
        return validate_data

