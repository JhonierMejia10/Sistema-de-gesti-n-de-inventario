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
    def crear_compra_service(ubicacion_entrega, proveedor, estado_compra, items, usuario_creador ,nota=None):
        from inventario.models import TipoMovimiento

        if not items or len(items) == 0:
            raise ValidationError("Debe incluir al menos un producto en la orden.")

        total = Decimal('0')
        for item in items:
            subtotal = item['cantidad'] * item['precio_unitario']
            total += subtotal

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
        except IntegrityError:
            raise ValidationError("Ya existe una orden de compra con esos datos.")

        # Manejador Bulk de Items y Stocks
        productos_ids = [item['producto'].id for item in items]
        
        # Bloqueamos los stocks existentes
        stocks_existentes = Stock.objects.select_for_update().filter(
            producto_id__in=productos_ids, 
            almacen=ubicacion_entrega
        )
        stock_dict = {stock.producto_id: stock for stock in stocks_existentes}

        items_a_crear = []
        movimientos_a_crear = []
        stocks_a_actualizar = []
        stocks_a_crear = []
        
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

            if estado_compra.nombre == 'Recibido':
                if producto.id in stock_dict:
                    # El stock ya existe, lo actualizamos
                    stock = stock_dict[producto.id]
                    saldo_anterior = stock.cantidad_en_mano
                    stock.cantidad_en_mano += cantidad
                    stocks_a_actualizar.append(stock)
                    saldo_nuevo = stock.cantidad_en_mano
                else:
                    # El stock no existe, debemos crearlo tras revisar que otro proceso no lo haya creado
                    # Usamos un try except para manejar la concurrencia a nivel de BD o lo encolamos para el bulk
                    saldo_anterior = 0
                    saldo_nuevo = cantidad
                    stocks_a_crear.append(
                        Stock(
                            producto=producto,
                            almacen=ubicacion_entrega,
                            cantidad_en_mano=cantidad
                        )
                    )

                movimientos_a_crear.append(
                    Movimiento(
                        usuario=usuario_creador,
                        tipo_movimiento_id=TipoMovimiento.ENTRADA,
                        producto=producto,
                        almacen=ubicacion_entrega,
                        cantidad=cantidad,
                        saldo_anterior=saldo_anterior,
                        saldo_nuevo=saldo_nuevo,
                        content_type=content_type_orden,
                        object_id=orden_compra.id,
                        nota=f"Entrada por orden de compra #{orden_compra.id}"
                    )
                )

        try:
            ItemOrdenCompra.objects.bulk_create(items_a_crear)
        except IntegrityError:
             raise ValidationError("Error al registrar los ítems. Posibles productos duplicados en la orden.")

        if estado_compra.nombre == 'Recibido':
            if stocks_a_actualizar:
                Stock.objects.bulk_update(stocks_a_actualizar, ['cantidad_en_mano'])
            
            if stocks_a_crear:
                # Si dos usuarios intentan recibir el mismo producto nuevo simultáneamente, bulk_create o el save fallará por Unique Constraint
                # Para mayor robustez en alta concurrencia usamos ignore_conflicts
                try:
                    Stock.objects.bulk_create(stocks_a_crear)
                except IntegrityError:
                    # En una arquitectura multi-hilo exacta aquí se podría re-correr la validación
                     raise ValidationError("Error de concurrencia creando stock inicial. Por favor, reintente la orden.")
            
            try:
                Movimiento.objects.bulk_create(movimientos_a_crear)
            except IntegrityError:
                raise ValidationError("Error al registrar los movimientos de inventario.")

        return orden_compra
    
    # @staticmethod
    # @transaction.atomic
    # def actualizar_orden(instance, data, usuario):
    #     """
    #     Actualiza campos simples, ítems parcialmente y ejecuta recepción si aplica.
    #     """

    #     estado_anterior = instance.estado_compra_id
    #     items_data = data.pop("items", None)
    #     items_a_eliminar = data.pop("items_a_eliminar", None)  # lista de ids de items a eliminar

    #     # --- 1. ACTUALIZAR CAMPOS SIMPLES ---
    #     for campo, valor in data.items():
    #         setattr(instance, campo, valor)
    #     instance.save()

    #     # --- 2. ELIMINAR ITEMS SI SE INDICA ---
    #     if items_a_eliminar:
    #         if estado_anterior == 2:
    #             raise ValidationError("No se pueden eliminar ítems de una orden ya recibida.")
    #         instance.itemordencompra_set.filter(id__in=items_a_eliminar).delete()

    #     # --- 3. ACTUALIZACIÓN PARCIAL DE ITEMS ---
    #     if items_data:
    #         if estado_anterior == 2:
    #             raise ValidationError("No se pueden modificar ítems de una orden ya recibida.")

    #         for item in items_data:
    #             producto = item['producto']
    #             cantidad = item['cantidad']
    #             precio_unitario = item['precio_unitario']

    #             obj, created = ItemOrdenCompra.objects.get_or_create(
    #                 orden_compra=instance,
    #                 producto=producto,
    #                 defaults={'cantidad': cantidad, 'precio_unitario': precio_unitario}
    #             )

    #             if not created:
    #                 # Actualiza cantidad y precio unitario
    #                 obj.cantidad = cantidad
    #                 obj.precio_unitario = precio_unitario
    #                 obj.save()

    #     # --- 4. RECALCULAR TOTAL ---
    #     total = Decimal('0')
    #     for item in instance.itemordencompra_set.all():
    #         total += item.cantidad * item.precio_unitario
    #     instance.total = total
    #     instance.save()

    #     # --- 5. DETECTAR RECEPCIÓN ---
    #     estado_nuevo = instance.estado_compra_id
    #     if estado_anterior != 2 and estado_nuevo == 2:
    #         CompraService._procesar_recepcion(instance, usuario)

    #     return instance

    # @staticmethod
    # def _procesar_recepcion(orden, usuario):
    #     """
    #     Cuando la orden pasa a estado 2: crear stock y movimientos.
    #     """
    #     for item in orden.itemordencompra_set.all():
    #         producto = item.producto
    #         cantidad = item.cantidad
    #         almacen = orden.ubicacion_entrega

    #         stock, created = Stock.objects.get_or_create(
    #             producto=producto,
    #             almacen=almacen,
    #             defaults={"cantidad_en_mano": 0}
    #         )

    #         saldo_anterior = stock.cantidad_en_mano
    #         saldo_nuevo = saldo_anterior + cantidad

    #         stock.cantidad_en_mano = saldo_nuevo
    #         stock.save()

    #         Movimiento.objects.create(
    #             usuario=usuario,
    #             tipo_movimiento_id=1,  # 1 = Entrada
    #             producto=producto,
    #             almacen=almacen,
    #             cantidad=cantidad,
    #             saldo_anterior=saldo_anterior,
    #             saldo_nuevo=saldo_nuevo,
    #             content_type=ContentType.objects.get_for_model(OrdenCompra),
    #             object_id=orden.id,
    #             nota=f"Entrada por orden de compra #{orden.id}"
    #         )