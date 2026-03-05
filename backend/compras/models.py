from django.db import models
from productos.models import Producto
from almacenes.models import Almacen
from core.models import EstadoPago
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - Telefono: {self.telefono} - Correo: {self.correo}"
    


from core.models import EstadoPago, TransaccionBase

class OrdenCompra(TransaccionBase):
    fecha_orden = models.DateTimeField(auto_now_add=True)
    fecha_esperada = models.DateField(null=True, blank=True)
    nota = models.TextField(blank=True, null=True)
    estado_pago = models.ForeignKey(
        EstadoPago,
        on_delete=models.PROTECT,
        db_index=True,
        related_name='ordenes_compra',
    )
    ubicacion_entrega = models.ForeignKey(
        Almacen,
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    class EstadoCompraChoices(models.TextChoices):
        PENDIENTE = 'Pendiente', 'Pendiente por recibir'
        RECIBIDO = 'Recibido', 'Recibido'
        CANCELADO = 'Cancelado', 'Cancelado'

    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ordenes_compra_creadas'
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT
    )
    estado_compra = models.CharField(
        max_length=20,
        choices=EstadoCompraChoices.choices,
        default=EstadoCompraChoices.PENDIENTE,
        db_index=True
    )

    class Meta:
        ordering = ['-fecha_orden']

    def __str__(self):
        return f"Orden de compra #{self.id} realizada al proveedor ({self.proveedor.nombre}) el día {self.fecha_orden.strftime('%Y-%m-%d')}" 
    
class ItemOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} "
    
    class Meta:
        unique_together = ('orden_compra', 'producto')