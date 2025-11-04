from rest_framework import serializers
from .models import Cliente, TipoCliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['id']

        extra_kwargs = {
            'nombre': {'required':True}
        }

class TipoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCliente
        fields = '__all__'
        read_only_fields = ['id']

        extra_kwargs = {
            'nombre': {'required':True}
        }