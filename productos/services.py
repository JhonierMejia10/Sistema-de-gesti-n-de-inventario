from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Producto
from inventario.models import Stock
from almacenes.models import Almacen
from django.db import IntegrityError


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
        except IntegrityError:
            raise ValidationError("Ya existe un producto con ese nombre.")

        try:
            stock_inicial = Stock.objects.create(
                producto=producto,
                almacen=almacen,
                cantidad_en_mano=stock_inicial
            )
        except IntegrityError:
            raise ValidationError("Ya existe un registro de stock para ese producto y almacén.")
        return producto

