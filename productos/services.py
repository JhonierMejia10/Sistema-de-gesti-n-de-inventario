from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import status
from .models import Producto
from inventario.models import Stock
from almacenes.models import Almacen


class ProductosService:
    
    @staticmethod
    @transaction.atomic
    def crear_producto_service(nombre, precio, categoria, marca, tipo_producto, stock_inicial, almacen, descripcion=None, foto=None, nota=None):

        try:
            producto = Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                foto=foto,
                categoria=categoria,
                marca=marca,
                tipo_producto=tipo_producto,
                nota=nota
            )
        except:
            raise ValidationError({'error':"No se pudo crear el producto. Compruebe los datos ingresados."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stock_inicial = Stock.objects.create(
                producto=producto,
                almacen=almacen,
                cantidad_en_mano=stock_inicial
            )
        except:
            raise ValidationError("Error, no se pudo crear el registro de stock inicial.")
        return producto

