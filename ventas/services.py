from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from .models import Orden, OrdenItem, Carrito, CarritoItem
from inventario.models import Movimiento, Stock
from pagos.models import PagoVenta
from django.db.models import Sum

class OrdenVentaService:

    @staticmethod
    @transaction.atomic
    def agregar_al_carrito(usuario_creador, cliente_id, almacen, producto, cantidad, precio_unitario):

        filtros = {
            'usuario_creador': usuario_creador,
            'almacen': almacen
        }

        if cliente_id is not None:
            filtros['cliente_id'] = cliente_id
        else:
            filtros['cliente__isnull'] = True
        
        try:
            carrito = Carrito.objects.filter(**filtros).first()
        except Carrito.DoesNotExist:
            if not carrito:
                raise ValidationError("No existe un carrito para este usuario / cliente / almacén")

        try:
            stock = Stock.objects.get(producto=producto, almacen=almacen)
        except Stock.DoesNotExist:
            raise ValidationError("No hay stock registrado para este producto en el almacén seleccionado.")

        cantidad_existente = carrito.items.filter(
            producto=producto
        ).aggregate(total=Sum("cantidad"))['total'] or 0

        total_solicitado = cantidad_existente + cantidad

        if total_solicitado > stock.cantidad_en_mano:
            raise ValidationError(
                f"Stock insuficiente. Disponible: {stock.cantidad_en_mano}, solicitado total: {total_solicitado}"
            )

        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={
                'cantidad': cantidad,
                'precio_unitario': precio_unitario
            }
        )

        if not created:
            item.cantidad += cantidad
            item.precio_unitario = precio_unitario  # opcional según negocio
            item.save()

        return item


