from django.db import transaction
from django.core.exceptions import ValidationError
from ventas.models import Orden
from .models import PagoVenta, PagoCompra
from compras.models import OrdenCompra

class PagoService:

    @staticmethod
    @transaction.atomic
    def registrar_pago_venta(orden, monto, metodo_pago, usuario, nota=None):
        """
        Registra un pago y actualiza el estado de la orden de venta ATÓMICAMENTE.
        """
        # Validar saldo (lock de la orden para evitar race conditions)
        orden = Orden.objects.select_for_update().get(pk=orden.pk)

        if monto > orden.saldo_pendiente:
            raise ValidationError(f"El pago excede el saldo. Disponible: ${orden.saldo_pendiente}")
        
        #Crear pago
        pago = PagoVenta.objects.create(
            orden=orden,
            monto=monto,
            metodo_pago=metodo_pago,
            registrado_por=usuario,
            nota=nota
        )

        #Actualizar total pagado y estado basado en cálculo
        orden.total_pagado += monto
        orden.estado_pago = orden.estado_pago_calculado
        orden.save(update_fields=['total_pagado', 'estado_pago'])

        return pago
    
    @staticmethod
    @transaction.atomic
    def registrar_pago_compra(orden_compra, monto, metodo_pago, usuario, nota=''):
        """
        Registra un pago y actualiza el estado de la orden de compra ATÓMICAMENTE.
        """
        orden_compra = OrdenCompra.objects.select_for_update().get(pk=orden_compra.pk)

        if monto > orden_compra.saldo_pendiente:
            raise ValidationError(f"El pago excede el saldo. Disponible: ${orden_compra.saldo_pendiente}")
        
        pago = PagoCompra.objects.create(
            orden_compra=orden_compra,
            monto=monto,
            metodo_pago=metodo_pago,
            registrado_por=usuario,
            nota=nota
        )

        orden_compra.total_pagado += monto
        orden_compra.estado_pago = orden_compra.estado_pago_calculado
        orden_compra.save(update_fields=['total_pagado', 'estado_pago'])

        return pago
