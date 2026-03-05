from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .models import Orden, OrdenItem
from inventario.models import Movimiento, Stock
from pagos.models import PagoVenta
from django.db import IntegrityError
from decimal import Decimal

class OrdenVentaService:

    @staticmethod
    @transaction.atomic
    def crear_orden_venta_service(almacen, items, cliente, usuario_creador, tipo_entrega, pago_inicial=Decimal('0'), metodo_pago=None, nota=None, direccion_envio=None):
        from inventario.models import Movimiento
        from inventario.services import InventarioService
        from pagos.services import PagoService
        
        if not items or len(items) == 0:
            raise ValidationError("Debes incluir al menos un producto en la orden.")
        
        total = Decimal('0')
        for item in items:
            subtotal = item['cantidad'] * item['precio_unitario']
            total += subtotal
        
        # Registrar en el modelo OrdenVenta
        try:
            orden_venta = Orden(
                almacen = almacen,
                cliente = cliente,
                usuario_creador = usuario_creador,
                tipo_entrega = tipo_entrega,
                total = total,
                total_pagado = Decimal('0'),
                nota = nota
            )
            orden_venta.estado_pago = orden_venta.estado_pago_calculado
            orden_venta.save()
        except IntegrityError:
            raise ValidationError("Ya existe una orden con esos datos.")

        orden_items_a_crear = []
        movimientos_data = []

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

            # Preparar datos para el movimiento de inventario
            movimientos_data.append({
                'producto': producto,
                'cantidad': cantidad,
                'tipo_movimiento': Movimiento.TipoMovimientoChoices.SALIDA,
                'nota': f"Salida por orden de venta #{orden_venta.id}"
            })

        # Ejecutar operaciones bulk de items
        try:
            OrdenItem.objects.bulk_create(orden_items_a_crear)
        except IntegrityError:
             raise ValidationError("Error al registrar los ítems de la orden. Verifica que no haya duplicados.")

        # Procesar movimientos de inventario usando el servicio centralizado
        InventarioService.procesar_movimientos_stock(
            almacen=almacen,
            movimientos_data=movimientos_data,
            usuario=usuario_creador,
            content_type_obj=content_type_orden,
            object_id=orden_venta.id
        )
        
        # Registrar pago inicial si aplica
        if pago_inicial and pago_inicial > 0:
            if not metodo_pago:
                raise ValidationError("Debe proporcionar un método de pago si hay un pago inicial.")
            PagoService.registrar_pago_venta(
                orden=orden_venta,
                monto=pago_inicial,
                metodo_pago=metodo_pago,
                usuario=usuario_creador,
                nota="Pago inicial registrado al crear la orden"
            )

        # --- Auto-crear Pedido si el tipo de entrega requiere envío ---
        TIPOS_CON_ENVIO = ['envío', 'envio', 'domicilio', 'pedido', 'delivery']
        requiere_envio = any(keyword in tipo_entrega.lower() for keyword in TIPOS_CON_ENVIO)

        if requiere_envio:
            from pedidos.models import Pedido
            
            estado_inicial = Pedido.EstadoPedidoChoices.PREPARANDO

            direccion = direccion_envio
            if not direccion and cliente:
                direccion = getattr(cliente, 'direccion', '') or ''
            if not direccion:
                raise ValidationError("Se requiere una dirección de envío para este tipo de entrega.")

            Pedido.objects.create(
                orden=orden_venta,
                estado=estado_inicial,
                direccion_envio=direccion,
                observaciones=nota or ''
            )

        return orden_venta
    
    @staticmethod
    @transaction.atomic
    def actualizar_orden_venta_service(orden_id, almacen, items, cliente, usuario_modificador, tipo_entrega, nota=None):
        from inventario.models import Movimiento
        from inventario.services import InventarioService
        
        if not items or len(items) == 0:
            raise ValidationError("Debes incluir al menos un producto en la orden.")
            
        try:
            orden = Orden.objects.get(id=orden_id)
        except Orden.DoesNotExist:
            raise ValidationError("La orden especificada no existe.")
            
        # 1. Actualizar cabecera de la orden
        orden.almacen = almacen
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
        
        orden_items_a_crear = []
        orden_items_a_actualizar = []
        movimientos_data = []
        
        content_type_orden = ContentType.objects.get_for_model(Orden)
        
        # --- PROCESAR ESCENARIO A: ÍTEMS BORRADOS (Devolver al stock) ---
        for prod_id in ids_borrados:
            item_borrado = items_actuales[prod_id]
            cantidad_a_devolver = item_borrado.cantidad
            
            movimientos_data.append({
                'producto': item_borrado.producto,
                'cantidad': cantidad_a_devolver,
                'tipo_movimiento': Movimiento.TipoMovimientoChoices.ENTRADA, # Regresa al inventario
                'nota': f"Entrada por ítem eliminado en edición de orden #{orden.id}"
            })
        
        # Eliminar items borrados de la BD
        if ids_borrados:
            OrdenItem.objects.filter(orden=orden, producto_id__in=ids_borrados).delete()

        # --- PROCESAR ESCENARIO B: ÍTEMS NUEVOS (Descontar del stock) ---
        for prod_id in ids_nuevos:
            item_nuevo = items_nuevos[prod_id]
            producto = item_nuevo['producto']
            cantidad_solicitada = item_nuevo['cantidad']
            precio_unitario = item_nuevo['precio_unitario']
            
            orden_items_a_crear.append(
                OrdenItem(
                    orden=orden,
                    producto=producto,
                    cantidad=cantidad_solicitada,
                    precio_unitario=precio_unitario
                )
            )
            
            movimientos_data.append({
                'producto': producto,
                'cantidad': cantidad_solicitada,
                'tipo_movimiento': Movimiento.TipoMovimientoChoices.SALIDA,
                'nota': f"Salida por ítem nuevo en edición de orden #{orden.id}"
            })

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
                if cantidad_nueva > cantidad_vieja:
                    # Necesitamos restar del stock la diferencia extra
                    diferencia = cantidad_nueva - cantidad_vieja
                    tipo_movimiento = Movimiento.TipoMovimientoChoices.SALIDA
                    nota_mov = f"Salida por aumento de cantidad en edición de orden #{orden.id}"
                else: 
                    # cantidad_nueva < cantidad_vieja
                    # Devolvemos al stock la diferencia
                    diferencia = cantidad_vieja - cantidad_nueva
                    tipo_movimiento = Movimiento.TipoMovimientoChoices.ENTRADA
                    nota_mov = f"Entrada por reducción de cantidad en edición de orden #{orden.id}"
                
                movimientos_data.append({
                    'producto': data_nueva['producto'],
                    'cantidad': diferencia,
                    'tipo_movimiento': tipo_movimiento,
                    'nota': nota_mov
                })

        # 4. Calcular el nuevo total
        total = Decimal('0')
        for item in items_nuevos.values():
            total += item['cantidad'] * item['precio_unitario']
        orden.total = total
        orden.estado_pago = orden.estado_pago_calculado

        # 5. Ejecutar operaciones en bloque en Base de Datos
        if orden_items_a_crear:
            OrdenItem.objects.bulk_create(orden_items_a_crear)
            
        if orden_items_a_actualizar:
            OrdenItem.objects.bulk_update(orden_items_a_actualizar, ['cantidad', 'precio_unitario'])
            
        if movimientos_data:
            InventarioService.procesar_movimientos_stock(
                almacen=almacen,
                movimientos_data=movimientos_data,
                usuario=usuario_modificador,
                content_type_obj=content_type_orden,
                object_id=orden.id
            )

        # Guardar cambios finales de la cabecera
        orden.save()
        
        return orden
    
