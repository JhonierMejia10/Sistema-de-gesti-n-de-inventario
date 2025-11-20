from django.db import models
from clientes.models import Cliente
from productos.models import Producto
from core.models import EstadoPago
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal

# Create your models here.


class TipoVenta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

class Carrito(models.Model):
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(decimal_places=2, max_digits=12)

    class Meta:
        unique_together = ('producto','cliente')
    
class Orden(models.Model):
    estado_pago = models.ForeignKey(
        EstadoPago,
        on_delete=models.PROTECT,
        db_index=True,
        related_name='ordenes_venta'
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ordenes_creadas'
    )
    tipo_venta = models.ForeignKey(
        TipoVenta,
        on_delete=models.CASCADE
    )
    total = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    fecha = models.DateField(db_index=True, auto_now_add=True)

    def total_pagado(self):
        return self.pagos.aggregate(Sum('monto'))['monto__sum'] or 0
    
    def saldo_pendiente(self):
        return self.total - self.total_pagado()
    
    @property
    def estado_pago_calculado(self):
        """
        Calcula el estado SIN modificar la BD.
        El servicio es responsable de guardarlo.
        """
        total_pagado = self.total_pagado()

        if total_pagado == Decimal('0'):
            return EstadoPago.obtener_pendiente()
        elif total_pagado >= self.total:
            return EstadoPago.obtener_completado()
        else:
            return EstadoPago.obtener_abonado()
    
    def __str__(self):
        return f"Orden #{self.id}"

    
class OrdenItem(models.Model):
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)

    #Restricción para que se cree una sola instancia de producto por cada orden
    class Meta:
        unique_together = ('orden','producto')


