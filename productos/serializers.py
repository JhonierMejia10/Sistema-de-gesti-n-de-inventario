from rest_framework import serializers
from categorias.models import Categoria
from proveedores.models import Proveedor
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','stock','categoria','proveedor']
        read_only_fields = ['id','fecha_creacion']

        extra_kwargs = {
            'nombre':{'required':True},
            'precio':{'required':True},
            'categoria':{'required':True}
        }
    
    def validate_stock(self, validate_data):
        if validate_data < 0:
            raise serializers.ValidationError("El stock no puede ser menor que cero")
        return validate_data
    
    def validate_precio(self, validate_data):
        if validate_data < 0:
            raise serializers.ValidationError("El valor no puede ser menor a cero")
        return validate_data

    def validate_categoria(self, validate_data):
        if not Categoria.objects.filter(nombre=validate_data).exists():
            raise serializers.ValidationError("La categoría seleccionada no existe")
        return validate_data
    