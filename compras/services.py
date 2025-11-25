from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .models import OrdenCompra
from .models import ItemOrdenCompra
from inventario.models import Movimiento, Stock
from core.models import EstadoPago

from decimal import Decimal

class CompraService:

    @staticmethod
    @transaction.atomic
    def crear_compra_service(ubicacion_entrega, proveedor, estado_compra, items, usuario_creador ,nota=None):

        if not items or len(items) == 0:
            raise ValidationError("Debe incluir al menos un producto en la orden.")

        total = Decimal('0')
        for item in items:
            subtotal = item['cantidad'] * item['precio_unitario']
            total += subtotal

        #Registrar en el modelo OrdenCompra
        try:
            orden_compra = OrdenCompra.objects.create(
                estado_compra = estado_compra,
                ubicacion_entrega = ubicacion_entrega,
                proveedor = proveedor,
                estado_pago = EstadoPago.obtener_pendiente(),
                nota = nota,
                total = total,
                usuario_creador = usuario_creador
            )
        except Exception as e:
            raise ValidationError(f"No se pudo crear la orden compra: {str(e)}")
        
        for item in items:
            producto = item['producto']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']

            #Registrar en el modelo ItemOrdenCompra
            try: 
                ItemOrdenCompra.objects.create(
                orden_compra = orden_compra,
                producto = producto,
                cantidad = cantidad,
                precio_unitario = precio_unitario
                )
            except Exception as e:
                raise ValidationError(f"Error al registrar producto {producto.nombre}: {str(e)}")


            #Si el estado de compra es igual al id = 2, el pedido ha sido recibido por lo tanto se podrá ingresar al inventario.
            if estado_compra.id == 2:
                try:
                    stock, created = Stock.objects.get_or_create(
                        producto = producto,
                        almacen = ubicacion_entrega,
                        defaults={'cantidad_en_mano': cantidad}
                    )
                    
                    # Manejar saldos según si el stock existía o no
                    if created:
                        saldo_anterior = 0
                        saldo_nuevo = cantidad
                    else:
                        saldo_anterior = stock.cantidad_en_mano
                        stock.cantidad_en_mano += cantidad
                        stock.save()
                        saldo_nuevo = stock.cantidad_en_mano

                except Exception as e:
                    raise ValidationError(f"No se pudo actualizar stock de {producto.nombre}: {str(e)}")
                
                try:
                    Movimiento.objects.create(
                        usuario = usuario_creador,
                        tipo_movimiento_id = 1,
                        producto = producto,
                        almacen = ubicacion_entrega,
                        cantidad = cantidad,
                        saldo_anterior = saldo_anterior,
                        saldo_nuevo = saldo_nuevo,
                        content_type = ContentType.objects.get_for_model(OrdenCompra),  # ← CORRECCIÓN AQUÍ
                        object_id = orden_compra.id,
                        nota = f"Entrada por orden de compra #{orden_compra.id}"
                    )
                except Exception as e:
                    raise ValidationError(f"Error al registrar movimiento de {producto.nombre}: {str(e)}")
        
        return orden_compra