from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from .models import Orden, OrdenItem
from inventario.models import Movimiento, Stock
from pagos.models import PagoVenta
from django.db import IntegrityError
from decimal import Decimal

class OrdenVentaService:

    @staticmethod
    @transaction.atomic
    def crear_orden_venta_service(almacen, estado_pago, items, cliente, usuario_creador, tipo_entrega, nota=None):
        from inventario.models import TipoMovimiento
        
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
                tipo_entrega = tipo_entrega,
                total = total,
                nota = nota
            )
        except IntegrityError:
            raise ValidationError("Ya existe una orden con esos datos.")

        # Obtener los ids de los productos para la consulta masiva de stock
        productos_ids = [item['producto'].id for item in items]

        # Validar y actualizar stock existente usando select_for_update
        stocks = Stock.objects.select_for_update().filter(
            producto_id__in=productos_ids, 
            almacen=almacen
        )
        stock_dict = {stock.producto_id: stock for stock in stocks}

        orden_items_a_crear = []
        movimientos_a_crear = []
        stocks_a_actualizar = []

        content_type_orden = ContentType.objects.get_for_model(Orden)

        for item in items:
            producto = item['producto']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']

            # Preparar creación del OrdenItem
            orden_items_a_crear.append(
                OrdenItem(
                    orden=orden_venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )
            )

            # Validar stock
            if producto.id not in stock_dict:
                raise ValidationError(
                    f"No existe stock registrado para el producto {producto.nombre} "
                    f"en el almacén seleccionado."
                )
            
            stock = stock_dict[producto.id]

            if stock.cantidad_en_mano < cantidad:
                raise ValidationError(
                    f"Stock insuficiente para {producto.nombre} en el almacén. "
                    f"Disponible: {stock.cantidad_en_mano}, Solicitado: {cantidad}"
                )

            saldo_anterior = stock.cantidad_en_mano
            stock.cantidad_en_mano -= cantidad
            stocks_a_actualizar.append(stock)
            saldo_nuevo = stock.cantidad_en_mano

            # Preparar creación del Movimiento
            movimientos_a_crear.append(
                Movimiento(
                    usuario=usuario_creador,
                    tipo_movimiento_id=TipoMovimiento.SALIDA,
                    producto=producto,
                    almacen=almacen,
                    cantidad=cantidad,
                    saldo_anterior=saldo_anterior,
                    saldo_nuevo=saldo_nuevo,
                    content_type=content_type_orden,
                    object_id=orden_venta.id,
                    nota=f"Salida por orden de venta #{orden_venta.id}"
                )
            )

        # Ejecutar operaciones bulk en la base de datos
        try:
            OrdenItem.objects.bulk_create(orden_items_a_crear)
        except IntegrityError:
             raise ValidationError("Error al registrar los ítems de la orden. Verifica que no haya duplicados.")

        try:
            Stock.objects.bulk_update(stocks_a_actualizar, ['cantidad_en_mano'])
        except IntegrityError:
             raise ValidationError("Error al actualizar el stock de los productos.")

        try:
            Movimiento.objects.bulk_create(movimientos_a_crear)
        except IntegrityError:
            raise ValidationError("Error al registrar los movimientos de inventario.")

        return orden_venta
    

    # @staticmethod
    # @transaction.atomic
    # def actualizar_orden_venta(instance, data, usuario):

    #     items_data = data.pop("items", None)

    #     # Actualizar campos simples
    #     for campo, valor in data.items():
    #         setattr(instance, campo, valor)
    #     instance.save()

    #     if items_data:
    #         for item in items_data:
    #             producto = item['producto']
    #             cantidad = item['cantidad']
    #             precio_unitario = item['precio_unitario']

    #             obj, created = OrdenItem.objects.get_or_create(
    #                 orden=instance,
    #                 producto=producto,
    #                 defaults={
    #                     'cantidad': cantidad,
    #                     'precio_unitario': precio_unitario
    #                 }
    #             )

    #             if not created:
    #                 obj.cantidad = cantidad
    #                 obj.precio_unitario = precio_unitario
    #                 obj.save()

    #     # Recalcular total
    #     total = Decimal('0')
    #     for item in instance.items.all():
    #         total += item.cantidad * item.precio_unitario

    #     instance.total = total
    #     instance.save()

    #     return instance


