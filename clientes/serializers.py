from rest_framework import serializers
from .models import Cliente, TipoCliente


class TipoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCliente
        fields = ['id', 'nombre', 'descripcion']

        extra_kwargs = {
            'id':{'read_only':True}
        }

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['id']


