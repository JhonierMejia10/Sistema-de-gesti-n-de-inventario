from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from .models import Stock, Movimiento

class InventarioService:
    @staticmethod
    def procesar_movimientos_stock(
        almacen, 
        movimientos_data, 
        usuario, 
        content_type_obj, 
        object_id, 
        es_recepcion_compra=False
    ):
        """
        Procesa una lista de movimientos para actualizar stock y crear los registros de Movimiento.
        
        movimientos_data debe ser una lista de diccionarios con la estructura:
        {
            'producto': Instancia del modelo Producto,
            'cantidad': Positivo entero,
            'tipo_movimiento': Movimiento.TipoMovimientoChoices.ENTRADA o SALIDA,
            'nota': String para el movimiento
        }
        es_recepcion_compra: Si es True, permite crear un registro de Stock si no existía previamente.
        """
        if not movimientos_data:
            return

        productos_ids = [data['producto'].id for data in movimientos_data]
        
        # Bloquear los stocks existentes
        stocks_existentes = Stock.objects.select_for_update().filter(
            producto_id__in=productos_ids, 
            almacen=almacen
        )
        stock_dict = {stock.producto_id: stock for stock in stocks_existentes}

        movimientos_a_crear = []
        stocks_a_actualizar = []
        stocks_a_crear = []

        for data in movimientos_data:
            producto = data['producto']
            cantidad = data['cantidad']
            tipo_movimiento = data['tipo_movimiento']
            nota = data.get('nota', '')

            if producto.id in stock_dict:
                stock = stock_dict[producto.id]
                saldo_anterior = stock.cantidad_en_mano
                
                if tipo_movimiento == Movimiento.TipoMovimientoChoices.ENTRADA:
                    stock.cantidad_en_mano += cantidad
                else: # SALIDA
                    if stock.cantidad_en_mano < cantidad:
                        raise ValidationError(f"Stock insuficiente para {producto.nombre}. Disponible: {stock.cantidad_en_mano}")
                    stock.cantidad_en_mano -= cantidad
                    
                saldo_nuevo = stock.cantidad_en_mano
                stocks_a_actualizar.append(stock)
            else:
                if es_recepcion_compra:
                    if tipo_movimiento != Movimiento.TipoMovimientoChoices.ENTRADA:
                        raise ValidationError(f"Intento de sacar inventario sin stock para {producto.nombre}.")
                    
                    saldo_anterior = 0
                    saldo_nuevo = cantidad
                    nuevo_stock = Stock(
                        producto=producto,
                        almacen=almacen,
                        cantidad_en_mano=cantidad
                    )
                    stocks_a_crear.append(nuevo_stock)
                    # Añadir al dict por si hay otro item igual en la misma orden
                    stock_dict[producto.id] = nuevo_stock 
                else:
                    raise ValidationError(f"No existe stock registrado para el producto {producto.nombre} en este almacén.")

            movimientos_a_crear.append(
                Movimiento(
                    usuario=usuario,
                    tipo_movimiento=tipo_movimiento,
                    producto=producto,
                    almacen=almacen,
                    cantidad=cantidad,
                    saldo_anterior=saldo_anterior,
                    saldo_nuevo=saldo_nuevo,
                    content_type=content_type_obj,
                    object_id=object_id,
                    nota=nota
                )
            )

        if stocks_a_actualizar:
            # Eliminar duplicados en caso de que un producto venga varias veces en la lista
            unique_stocks_actualizar = {s.producto_id: s for s in stocks_a_actualizar}.values()
            Stock.objects.bulk_update(unique_stocks_actualizar, ['cantidad_en_mano'])
            
        if stocks_a_crear:
            try:
                Stock.objects.bulk_create(stocks_a_crear)
            except IntegrityError:
                raise ValidationError("Error de concurrencia creando stock inicial. Por favor, reintente la orden.")
        
        if movimientos_a_crear:
            try:
                Movimiento.objects.bulk_create(movimientos_a_crear)
            except IntegrityError:
                raise ValidationError("Error al registrar los movimientos de inventario.")

