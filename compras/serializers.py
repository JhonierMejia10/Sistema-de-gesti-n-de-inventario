from rest_framework import serializers
from .models import Proveedor, EstadoCompra, OrdenCompra, ItemOrdenCompra

class ProveedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = '__all__'

        extra_kwargs = {
            'nombre':{'required':True}
        }
    
    def validate_nombre(self,validate_data):

        if self.instance:
            if Proveedor.objects.filter(nombre=validate_data).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Ya existe un proveedor con este nombre.")

        else:
            if Proveedor.objects.filter(nombre=validate_data).exists():
                raise serializers.ValidationError("Ya existe un proveedor con este nombre.")
        return validate_data
        

class EstadoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCompra
        fields = '__all__'
        
        extra_kwargs = {
            'nombre':{'required':True}
        }

        def validate_nombre(self,validate_data):

            if self.instance:
                if EstadoCompra.objects.filter(nombre=validate_data).exclude(id=self.instance.id).exists():
                    raise serializers.ValidationError("Ya existe un estado de compra con este nombre.")
            else:
                if EstadoCompra.objects.filter(nombre=validate_data):
                    raise serializers.ValidationError("Ya existe un estado de compra con este nombre.")
            return validate_data


class OrdenCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenCompra
        fields = '__all__'

        extra_kwargs = {
            'fecha_orden':{'read_only':True},
            'usuario_creador':{'read_only':True}
        }


class ItemoOrdenCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrdenCompra
        fields = '__all__'


    