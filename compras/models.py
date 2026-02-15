from django.db import models
from productos.models import Producto
from almacenes.models import Almacen
from core.models import EstadoPago
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True)
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - Telefono: {self.telefono} - Correo: {self.correo}"
    
class EstadoCompra(models.Model):
    nombre = models.CharField(max_length=50, unique=True, null=False, blank=False)
    descripcion = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    fecha_orden = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    nota = models.TextField(blank=True, null=True)
    estado_pago = models.ForeignKey(
        EstadoPago,
        on_delete=models.PROTECT,
        db_index=True,
        related_name='ordenes_compra',
        default=3
    )
    ubicacion_entrega = models.ForeignKey(
        Almacen,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ordenes_compra_creadas'
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE
    )
    estado_compra = models.ForeignKey(
        EstadoCompra,
        on_delete=models.CASCADE,
        default=1
    )

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
        total_pagado= self.total_pagado()

        if total_pagado == Decimal('0'):
            return EstadoPago.obtener_pendiente()
        elif total_pagado >= self.total:
            return EstadoPago.obtener_completado()
        else:
            return EstadoPago.obtener_abonado()

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