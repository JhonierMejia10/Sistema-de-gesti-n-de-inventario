from rest_framework import serializers
from .models import EstadoPedido, Pedido, PedidoItem


class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPedido
        fields = '__all__'
        extra_kwargs = {
            'nombre':{'required':True}
        }

    def validate_nombre(self, validate_data):

        if self.instance:
            if EstadoPedido.objects.filter(nombre=validate_data).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Este estado ya existe.")
        else:
            if EstadoPedido.objects.filter(nombre=validate_data).exists():
                raise serializers.ValidationError("Este estado ya existe.")
        return validate_data


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoItem
        fields = '__all__'