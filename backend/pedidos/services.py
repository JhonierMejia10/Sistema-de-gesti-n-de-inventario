from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from .models import Pedido
from inventario.models import Stock, Movimiento
from ventas.models import Orden

class PedidoService:
    @staticmethod
    @transaction.atomic
    def actualizar_pedido_service(pedido_id, nuevo_estado, observaciones, usuario_modificador):
        pedido = Pedido.objects.select_related('orden', 'orden__almacen').get(id=pedido_id)
        estado_viejo = pedido.estado

        # Prevenir modificación si ya estaba en estado terminal
        terminal_states = [Pedido.EstadoPedidoChoices.CANCELADO, Pedido.EstadoPedidoChoices.ENTREGADO]
        if estado_viejo in terminal_states and estado_viejo != nuevo_estado:
            raise ValidationError(f"No se puede cambiar el estado de un pedido que ya está '{estado_viejo}'.")

        # Si transiciona a Cancelado por primera vez
        if nuevo_estado == Pedido.EstadoPedidoChoices.CANCELADO and estado_viejo != Pedido.EstadoPedidoChoices.CANCELADO:
            orden = pedido.orden
            almacen = orden.almacen
            
            # Devolver stock
            items = orden.items.all()
            productos_ids = [item.producto_id for item in items]
            
            movimientos_data = []
            content_type_orden = ContentType.objects.get_for_model(Orden)
            
            for item in items:
                movimientos_data.append({
                    'producto': item.producto,
                    'cantidad': item.cantidad,
                    'tipo_movimiento': Movimiento.TipoMovimientoChoices.ENTRADA, # Regresa al inventario
                    'nota': f"Entrada por cancelación logística de Pedido #{pedido.id} (Orden V-{orden.id})"
                })
                    
            if movimientos_data:
                from inventario.services import InventarioService
                InventarioService.procesar_movimientos_stock(
                    almacen=almacen,
                    movimientos_data=movimientos_data,
                    usuario=usuario_modificador,
                    content_type_obj=content_type_orden,
                    object_id=orden.id
                )

        # Actualizar datos del pedido
        pedido.estado = nuevo_estado
        if observaciones is not None:
            pedido.observaciones = observaciones
        pedido.save()
        
        return pedido
