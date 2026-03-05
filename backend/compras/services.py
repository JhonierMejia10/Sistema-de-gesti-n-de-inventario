from django.db import transaction, IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .models import OrdenCompra, ItemOrdenCompra
from inventario.models import Movimiento, Stock
from core.models import EstadoPago
from decimal import Decimal

class CompraService:

    @staticmethod
    @transaction.atomic
    def crear_compra_service(ubicacion_entrega, proveedor, estado_compra, items, usuario_creador, fecha_esperada=None, pago_inicial=Decimal('0'), metodo_pago=None, nota=None):
        from inventario.models import Movimiento
        from inventario.services import InventarioService
        from pagos.services import PagoService

        if not items or len(items) == 0:
            raise ValidationError("Debe incluir al menos un producto en la orden.")

        total = Decimal('0')
        for item in items:
            subtotal = item['cantidad'] * item['precio_unitario']
            total += subtotal

        try:
            orden_compra = OrdenCompra(
                estado_compra = estado_compra,
                ubicacion_entrega = ubicacion_entrega,
                proveedor = proveedor,
                nota = nota,
                fecha_esperada = fecha_esperada,
                total = total,
                total_pagado = Decimal('0'),
                usuario_creador = usuario_creador
            )
            orden_compra.estado_pago = orden_compra.estado_pago_calculado
            orden_compra.save()
        except IntegrityError:
            raise ValidationError("Ya existe una orden de compra con esos datos.")

        items_a_crear = []
        movimientos_data = []
        
        content_type_orden = ContentType.objects.get_for_model(OrdenCompra)

        for item in items:
            producto = item['producto']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']

            items_a_crear.append(
                ItemOrdenCompra(
                    orden_compra=orden_compra,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )
            )

            if estado_compra == OrdenCompra.EstadoCompraChoices.RECIBIDO:
                movimientos_data.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'tipo_movimiento': Movimiento.TipoMovimientoChoices.ENTRADA,
                    'nota': f"Entrada por orden de compra #{orden_compra.id}"
                })

        try:
            ItemOrdenCompra.objects.bulk_create(items_a_crear)
        except IntegrityError:
             raise ValidationError("Error al registrar los ítems. Posibles productos duplicados en la orden.")

        if estado_compra == OrdenCompra.EstadoCompraChoices.RECIBIDO and movimientos_data:
            InventarioService.procesar_movimientos_stock(
                almacen=ubicacion_entrega,
                movimientos_data=movimientos_data,
                usuario=usuario_creador,
                content_type_obj=content_type_orden,
                object_id=orden_compra.id,
                es_recepcion_compra=True
            )
            
        # Registrar pago inicial si aplica
        if pago_inicial and pago_inicial > 0:
            if not metodo_pago:
                raise ValidationError("Debe proporcionar un método de pago si hay un pago inicial.")
            PagoService.registrar_pago_compra(
                orden_compra=orden_compra,
                monto=pago_inicial,
                metodo_pago=metodo_pago,
                usuario=usuario_creador,
                nota="Pago inicial registrado al crear la orden"
            )

        return orden_compra

    @staticmethod
    @transaction.atomic
    def actualizar_orden_compra_service(orden_id, estado_compra, usuario, nota=None):
        """
        Actualiza el estado logístico y la nota de una orden de compra.
        Si la orden transiciona a 'Recibido', ejecuta la recepción de inventario.
        """


        try:
            orden = OrdenCompra.objects.select_for_update().get(pk=orden_id)
        except OrdenCompra.DoesNotExist:
            raise ValidationError("La orden de compra especificada no existe.")

        estado_anterior = orden.estado_compra

        # No permitir modificar una orden ya recibida
        if estado_anterior == OrdenCompra.EstadoCompraChoices.RECIBIDO:
            raise ValidationError("No se puede modificar una orden que ya fue recibida.")

        # Actualizar campos editables
        orden.estado_compra = estado_compra
        if nota is not None:
            orden.nota = nota

        # Si transiciona a "Recibido", procesar la recepción de inventario
        if estado_compra == OrdenCompra.EstadoCompraChoices.RECIBIDO:
            CompraService._procesar_recepcion(orden, usuario)

        orden.save()
        return orden

    @staticmethod
    def _procesar_recepcion(orden, usuario):
        """
        Cuando la orden pasa a 'Recibido': crear/actualizar stock y registrar movimientos de entrada.
        Usa bulk operations para eficiencia.
        """
        from inventario.models import Movimiento
        from inventario.services import InventarioService

        items = orden.items.select_related('producto').all()
        if not items.exists():
            raise ValidationError("La orden no tiene ítems para recibir.")

        almacen = orden.ubicacion_entrega
        movimientos_data = []

        content_type_orden = ContentType.objects.get_for_model(OrdenCompra)

        for item in items:
            movimientos_data.append({
                'producto': item.producto,
                'cantidad': item.cantidad,
                'tipo_movimiento': Movimiento.TipoMovimientoChoices.ENTRADA,
                'nota': f"Entrada por recepción de orden de compra #{orden.id}"
            })

        if movimientos_data:
            InventarioService.procesar_movimientos_stock(
                almacen=almacen,
                movimientos_data=movimientos_data,
                usuario=usuario,
                content_type_obj=content_type_orden,
                object_id=orden.id,
                es_recepcion_compra=True
            )