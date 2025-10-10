from rest_framework import serializers
from .models import Carrito, Orden, OrdenItem
from django.contrib.auth.models import User

class CarritoSerializer(serializers.ModelSerializer):
    
    usuario_creador = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )

    def validate(self, data):
        data['precio'] = data['cantidad']* data['precio_unitario']
        return data
    
    class Meta:
        model = Carrito
        fields = ['cliente','producto','cantidad','precio_unitario','precio']
        extra_kwargs = {
            'precio':{'read_only':True},
            'usuario_creador':{'read_only':True}
        }


    

