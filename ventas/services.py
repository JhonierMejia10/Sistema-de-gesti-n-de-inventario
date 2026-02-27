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
    
    @staticmethod
    @transaction.atomic
    def actualizar_orden_venta_service(orden_id, almacen, estado_pago, items, cliente, usuario_modificador, tipo_entrega, nota=None):
        from inventario.models import TipoMovimiento
        
        if not items or len(items) == 0:
            raise ValidationError("Debes incluir al menos un producto en la orden.")
            
        try:
            orden = Orden.objects.get(id=orden_id)
        except Orden.DoesNotExist:
            raise ValidationError("La orden especificada no existe.")
            
        # 1. Actualizar cabecera de la orden
        orden.almacen = almacen
        orden.estado_pago = estado_pago
        orden.cliente = cliente
        orden.tipo_entrega = tipo_entrega
        orden.nota = nota
        
        # 2. Obtener estado actual de los ítems en base de datos
        items_actuales = {item.producto_id: item for item in orden.items.all()}
        
        # 3. Mapear nuevos ítems del request
        items_nuevos = {item['producto'].id: item for item in items}
        
        # Identificar los 3 escenarios
        ids_borrados = set(items_actuales.keys()) - set(items_nuevos.keys())
        ids_nuevos = set(items_nuevos.keys()) - set(items_actuales.keys())
        ids_mantenidos = set(items_actuales.keys()).intersection(set(items_nuevos.keys()))
        
        # Obtener todos los productos afectados para consultar el stock (borrados, nuevos, o cantidad cambiada)
        productos_afectados_ids = set()
        
        for p_id in ids_borrados: productos_afectados_ids.add(p_id)
        for p_id in ids_nuevos: productos_afectados_ids.add(p_id)
        for p_id in ids_mantenidos:
            if items_actuales[p_id].cantidad != items_nuevos[p_id]['cantidad']:
                productos_afectados_ids.add(p_id)
        
        # Bloquear y obtener stock actual solo de los que van a cambiar cantidad
        stocks = Stock.objects.select_for_update().filter(
            producto_id__in=productos_afectados_ids, 
            almacen=almacen
        )
        stock_dict = {stock.producto_id: stock for stock in stocks}
        
        orden_items_a_crear = []
        orden_items_a_actualizar = []
        movimientos_a_crear = []
        stocks_a_actualizar = []
        
        content_type_orden = ContentType.objects.get_for_model(Orden)
        
        # --- PROCESAR ESCENARIO A: ÍTEMS BORRADOS (Devolver al stock) ---
        for prod_id in ids_borrados:
            item_borrado = items_actuales[prod_id]
            cantidad_a_devolver = item_borrado.cantidad
            
            if prod_id in stock_dict:
                stock = stock_dict[prod_id]
                saldo_anterior = stock.cantidad_en_mano
                stock.cantidad_en_mano += cantidad_a_devolver
                saldo_nuevo = stock.cantidad_en_mano
                stocks_a_actualizar.append(stock)
                
                movimientos_a_crear.append(
                    Movimiento(
                        usuario=usuario_modificador,
                        tipo_movimiento_id=TipoMovimiento.ENTRADA, # Regresa al inventario
                        producto=item_borrado.producto,
                        almacen=almacen,
                        cantidad=cantidad_a_devolver,
                        saldo_anterior=saldo_anterior,
                        saldo_nuevo=saldo_nuevo,
                        content_type=content_type_orden,
                        object_id=orden.id,
                        nota=f"Entrada por ítem eliminado en edición de orden #{orden.id}"
                    )
                )
        
        # Eliminar items borrados de la BD
        if ids_borrados:
            OrdenItem.objects.filter(orden=orden, producto_id__in=ids_borrados).delete()

        # --- PROCESAR ESCENARIO B: ÍTEMS NUEVOS (Descontar del stock) ---
        for prod_id in ids_nuevos:
            item_nuevo = items_nuevos[prod_id]
            producto = item_nuevo['producto']
            cantidad_solicitada = item_nuevo['cantidad']
            precio_unitario = item_nuevo['precio_unitario']
            
            if prod_id not in stock_dict:
                 raise ValidationError(f"No existe stock para el producto {producto.nombre} en este almacén.")
            
            stock = stock_dict[prod_id]
            
            if stock.cantidad_en_mano < cantidad_solicitada:
                raise ValidationError(f"Stock insuficiente para {producto.nombre}. Disponible: {stock.cantidad_en_mano}")
                
            saldo_anterior = stock.cantidad_en_mano
            stock.cantidad_en_mano -= cantidad_solicitada
            saldo_nuevo = stock.cantidad_en_mano
            stocks_a_actualizar.append(stock)
            
            orden_items_a_crear.append(
                OrdenItem(
                    orden=orden,
                    producto=producto,
                    cantidad=cantidad_solicitada,
                    precio_unitario=precio_unitario
                )
            )
            
            movimientos_a_crear.append(
                Movimiento(
                    usuario=usuario_modificador,
                    tipo_movimiento_id=TipoMovimiento.SALIDA,
                    producto=producto,
                    almacen=almacen,
                    cantidad=cantidad_solicitada,
                    saldo_anterior=saldo_anterior,
                    saldo_nuevo=saldo_nuevo,
                    content_type=content_type_orden,
                    object_id=orden.id,
                    nota=f"Salida por ítem nuevo en edición de orden #{orden.id}"
                )
            )

        # --- PROCESAR ESCENARIO C: ÍTEMS MANTENIDOS (Ajustar diferencias) ---
        for prod_id in ids_mantenidos:
            item_actual = items_actuales[prod_id]
            data_nueva = items_nuevos[prod_id]
            
            cantidad_vieja = item_actual.cantidad
            cantidad_nueva = data_nueva['cantidad']
            
            # Actualizar datos en memoria para el item
            item_actual.cantidad = cantidad_nueva
            item_actual.precio_unitario = data_nueva['precio_unitario']
            orden_items_a_actualizar.append(item_actual)
            
            if cantidad_vieja != cantidad_nueva:
                stock = stock_dict[prod_id]
                saldo_anterior = stock.cantidad_en_mano
                
                if cantidad_nueva > cantidad_vieja:
                    # Necesitamos restar del stock la diferencia extra
                    diferencia = cantidad_nueva - cantidad_vieja
                    if stock.cantidad_en_mano < diferencia:
                         raise ValidationError(f"Stock insuficiente para aumentar {data_nueva['producto'].nombre}.")
                    stock.cantidad_en_mano -= diferencia
                    tipo_movimiento = TipoMovimiento.SALIDA
                    nota_mov = f"Salida por aumento de cantidad en edición de orden #{orden.id}"
                    
                else: 
                    # cantidad_nueva < cantidad_vieja
                    # Devolvemos al stock la diferencia
                    diferencia = cantidad_vieja - cantidad_nueva
                    stock.cantidad_en_mano += diferencia
                    tipo_movimiento = TipoMovimiento.ENTRADA
                    nota_mov = f"Entrada por reducción de cantidad en edición de orden #{orden.id}"
                
                saldo_nuevo = stock.cantidad_en_mano
                # Solo agregar si no fue agregado antes en este mismo ciclo
                if stock not in stocks_a_actualizar: 
                    stocks_a_actualizar.append(stock)
                
                movimientos_a_crear.append(
                    Movimiento(
                        usuario=usuario_modificador,
                        tipo_movimiento_id=tipo_movimiento,
                        producto=data_nueva['producto'],
                        almacen=almacen,
                        cantidad=diferencia,
                        saldo_anterior=saldo_anterior,
                        saldo_nuevo=saldo_nuevo,
                        content_type=content_type_orden,
                        object_id=orden.id,
                        nota=nota_mov
                    )
                )

        # 4. Calcular el nuevo total
        total = Decimal('0')
        for item in items_nuevos.values():
            total += item['cantidad'] * item['precio_unitario']
        orden.total = total

        # 5. Ejecutar operaciones en bloque en Base de Datos
        if orden_items_a_crear:
            OrdenItem.objects.bulk_create(orden_items_a_crear)
            
        if orden_items_a_actualizar:
            OrdenItem.objects.bulk_update(orden_items_a_actualizar, ['cantidad', 'precio_unitario'])
            
        # Para que no de error si bulk_update recibe el mismo stock 2 veces
        if stocks_a_actualizar:
             # Eliminar duplicados de la lista manteniendo el último estado 
             # (aunque aquí cada stock_id debería ser único por cómo usamos stock_dict)
             unique_stocks = {s.producto_id: s for s in stocks_a_actualizar}.values()
             Stock.objects.bulk_update(unique_stocks, ['cantidad_en_mano'])
             
        if movimientos_a_crear:
            Movimiento.objects.bulk_create(movimientos_a_crear)

        # Guardar cambios finales de la cabecera
        orden.save()
        
        return orden
    
