from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from .models import Orden, OrdenItem
from inventario.models import Movimiento, Stock
from pagos.models import PagoVenta
from django.db.models import Sum

from decimal import Decimal

class OrdenVentaService:

    @staticmethod
    @transaction.atomic
    def crear_orden_venta_service(almacen, estado_pago, items, cliente, usuario_creador, tipo_venta, nota=None):
        
        if not items or len(items) == 0:
            raise ValidationError("Debes incluir al menos un producto en la orden.")
        
        total = Decimal('0')
        for item in items:
            subtotal = item['cantidad'] * item['precio_unitario']
            total += subtotal
        
        #Registrar en el modelo OrdenVenta
        try:
            orden_venta = Orden.objects.create(
                estado_pago = estado_pago,
                almacen = almacen,
                cliente = cliente,
                usuario_creador = usuario_creador,
                tipo_venta = tipo_venta,
                total = total,
                nota = nota
            )
        except Exception as e:
            raise ValidationError(f"No se pudo crear la orden de venta: {str(e)}")

        for item in items:
            producto = item['producto']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']

            #Registrar en el modelo ItemOrdenVenta
            try:
                OrdenItem.objects.create(
                    orden = orden_venta,
                    producto = producto,
                    cantidad = cantidad,
                    precio_unitario = precio_unitario
                )
            except Exception as e:
                raise ValidationError(f"Error al registrar producto {producto.nombre}: {str(e)}")

            #Registrar nuevo stock
            try:
                stock = Stock.objects.get_or_create(
                    producto = producto,
                    almacen = almacen,
                    defaults={'cantidad_en_mano':cantidad}
                )
                saldo_anterior = stock.cantidad_en_mano
                stock.cantidad_en_mano -= cantidad
                stock.save()
                saldo_nuevo = stock.cantidad_en_mano
            except Exception as e:
                raise ValidationError(f"No se pudo actualizar el stock de {producto.nombre}: {str(e)}")

            #Registrar movimiento de producto
            try:
                Movimiento.objects.create(
                    usuario = usuario_creador,
                    tipo_movimiento = 2,
                    producto = producto,
                    almacen = almacen,
                    cantidad = cantidad,
                    saldo_anterior = saldo_anterior,
                    saldo_nuevo = saldo_nuevo,
                    content_type = ContentType.objects.get_for_model(Orden),
                    object_id = orden_venta.id,
                    nota = f"Salida por orden de venta #{orden_venta.id}"
                )
            except Exception as e:
                raise ValidationError(f"Error al registrar movimiento de {producto.nombre}: {str(e)}")
        return orden_venta
    

@staticmethod
@transaction.atomic
def actualizar_orden_venta(instance, data, usuario):
    """
    Docstring para actualizar_orden_venta, actualizar campos como productos y cantidad
    
    :param instance: Descripción
    :param data: Descripción
    :param usuario: Descripción
    """

    items_data = data.pop("items", None)
    
    #Actualizar campos
    for campo, valor in data.items():
        setattr(instance, campo, valor)
    instance.save()

    if items_data:
        for item in items_data:
            producto = item['producto']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']
        
        obj, created = OrdenItem.objects.get_or_create(
            orden = instance,
            producto = producto,
            defaults={'cantidad': cantidad, 'precio_unitario':precio_unitario}
        )
        if not created:
            #Actualiza cantidad y precio unitario
            obj.cantidad = cantidad,
            obj.precio_unitario = precio_unitario,
            obj.save()
    
    #Recalcular total
    total = Decimal('0')
    for item in instance.ordenitem_set.all():
        total += item.cantidad * item.precio_unitario
    instance.total = total
    instance.save()

    return instance

