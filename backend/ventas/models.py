from django.db import models
from clientes.models import Cliente
from productos.models import Producto
from core.models import EstadoPago
from almacenes.models import Almacen
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal


from core.models import EstadoPago, TransaccionBase

class Orden(TransaccionBase):
    estado_pago = models.ForeignKey(
        EstadoPago,
        on_delete=models.PROTECT,
        db_index=True,
        related_name='ordenes_venta'
    )
    almacen = models.ForeignKey(
        Almacen,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    class TipoEntregaChoices(models.TextChoices):
        CAJA = 'Caja', 'Entrega en caja'
        PEDIDO = 'Pedido', 'Envío a domicilio'

    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ordenes_creadas'
    )
    tipo_entrega = models.CharField(
        max_length=20,
        choices=TipoEntregaChoices.choices,
        default=TipoEntregaChoices.CAJA,
        db_index=True
    )
    fecha = models.DateField(db_index=True, auto_now_add=True)
    nota = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha']

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
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    #Restricción para que se cree una sola instancia de producto por cada orden
    class Meta:
        unique_together = ('orden','producto')


