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


            #Si el estado de compra es igual al id = 2, el pedido ha sido recibido por lo tanto se podrá ingresar al inventario (Oportunidad de mejora).
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
                #El tipo de movimiento se establece desde el servicio por lo tanto es un registro que depende enteramente del código (Oportunidad de mejora). 
                try:
                    Movimiento.objects.create(
                        usuario = usuario_creador,
                        tipo_movimiento_id = 1,
                        producto = producto,
                        almacen = ubicacion_entrega,
                        cantidad = cantidad,
                        saldo_anterior = saldo_anterior,
                        saldo_nuevo = saldo_nuevo,
                        content_type = ContentType.objects.get_for_model(OrdenCompra),  
                        object_id = orden_compra.id,
                        nota = f"Entrada por orden de compra #{orden_compra.id}"
                    )
                except Exception as e:
                    raise ValidationError(f"Error al registrar movimiento de {producto.nombre}: {str(e)}")
        return orden_compra
    
    @staticmethod
    @transaction.atomic
    def actualizar_compra_service(orden_compra_id, estado_compra=None, items=None, usuario_modificador=None, **kwargs):

        # 1. Obtener la orden de compra con todas las relaciones
        try:
            orden_compra = OrdenCompra.objects.select_related(
                'estado_compra', 
                'ubicacion_entrega', 
                'proveedor',
                'estado_pago'
            ).get(id=orden_compra_id)
        except OrdenCompra.DoesNotExist:
            raise ValidationError("La orden de compra no existe.")
        
        estado_anterior = orden_compra.estado_compra
        
        # 2. Validar que se puede editar
        if estado_anterior.id == 2:
            if items is not None:
                raise ValidationError("No se pueden modificar items de una orden ya recibida.")
        
        # 3. Actualizar items si vienen
        total_actualizado = False
        if items is not None and estado_anterior.id != 2:
            CompraService._actualizar_items(orden_compra, items)
            # Recalcular total
            orden_compra.total = CompraService._calcular_total(orden_compra)
            total_actualizado = True
        
        # 4. Actualizar campos directamente en la instancia
        campos_modificados = []
        
        if estado_compra is not None:
            orden_compra.estado_compra = estado_compra
            campos_modificados.append('estado_compra')
        
        if total_actualizado:
            campos_modificados.append('total')
        
        if 'ubicacion_entrega' in kwargs:
            orden_compra.ubicacion_entrega = kwargs['ubicacion_entrega']
            campos_modificados.append('ubicacion_entrega')
        
        if 'proveedor' in kwargs:
            orden_compra.proveedor = kwargs['proveedor']
            campos_modificados.append('proveedor')
        
        if 'nota' in kwargs:
            orden_compra.nota = kwargs['nota']
            campos_modificados.append('nota')
        
        # 5. Guardar solo los campos modificados
        if campos_modificados:
            orden_compra.save(update_fields=campos_modificados)
        
        # 6. Si cambia a "Recibido", procesar stock
        if estado_compra and estado_compra.id == 2 and estado_anterior.id != 2:
            CompraService._procesar_recepcion_stock(orden_compra, usuario_modificador)
        
        return orden_compra
        
    
    @staticmethod
    @transaction.atomic
    def _actualizar_items(orden_compra, items_data):
        """
        Actualiza los items de la orden: elimina los anteriores y crea los nuevos
        Estrategia simple: reemplazar todos
        """
        if not items_data or len(items_data) == 0:
            raise ValidationError("Debe incluir al menos un producto en la orden.")
        
        # Eliminar items existentes
        ItemOrdenCompra.objects.filter(orden_compra=orden_compra).delete()
        
        # Crear nuevos items
        for item in items_data:
            try:
                ItemOrdenCompra.objects.create(
                    orden_compra=orden_compra,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario']
                )
            except Exception as e:
                raise ValidationError(f"Error al actualizar producto {item['producto'].nombre}: {str(e)}")
    
    @staticmethod
    @transaction.atomic
    def _calcular_total(orden_compra):
        """Calcula el total de la orden basado en sus items"""
        items = ItemOrdenCompra.objects.filter(orden_compra=orden_compra)
        total = sum(item.cantidad * item.precio_unitario for item in items)
        return Decimal(str(total))
    
    @staticmethod
    @transaction.atomic
    def _procesar_recepcion_stock(orden_compra, usuario):
        """
        Procesa la recepción: actualiza stock y crea movimientos
        (Reutiliza la lógica que ya tienes en crear_compra_service)
        """
        items = ItemOrdenCompra.objects.select_related('producto').filter(orden_compra=orden_compra)
        
        if not items.exists():
            raise ValidationError("La orden no tiene items para recepcionar.")
        
        for item in items:
            producto = item.producto
            cantidad = item.cantidad
            almacen = orden_compra.ubicacion_entrega
            
            # Actualizar stock
            try:
                stock, created = Stock.objects.get_or_create(
                    producto=producto,
                    almacen=almacen,
                    defaults={'cantidad_en_mano': cantidad}
                )
                
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
            
            # Crear movimiento
            try:
                Movimiento.objects.create(
                    usuario=usuario,
                    tipo_movimiento_id=1,
                    producto=producto,
                    almacen=almacen,
                    cantidad=cantidad,
                    saldo_anterior=saldo_anterior,
                    saldo_nuevo=saldo_nuevo,
                    content_type=ContentType.objects.get_for_model(OrdenCompra),
                    object_id=orden_compra.id,
                    nota=f"Entrada por recepción de orden de compra #{orden_compra.id}"
                )
            except Exception as e:
                raise ValidationError(f"Error al registrar movimiento de {producto.nombre}: {str(e)}")
    