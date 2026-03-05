
from django.db import models
from ventas .models import Orden
from compras .models import OrdenCompra
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum
from decimal import Decimal

# Create your models here.

#Este modelo se debe migrar a la aplicación core pero no se ha hecho debido a que puede generar retrasos
class MedioPago(models.Model):
    nombre = models.CharField(max_length=100, unique=True, db_index=True, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class PagoVenta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(decimal_places=2, max_digits=12)
    nota = models.TextField(blank=True,null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name='pagos'    
        )
    metodo_pago = models.ForeignKey(
        MedioPago,
        on_delete=models.PROTECT
    )
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='pagos_venta_registrados'
    )

    class Meta:
        indexes = [
            models.Index(fields=['orden','-fecha']),
        ]
        ordering = ['-fecha']
        verbose_name = 'Pago de venta'
        verbose_name_plural = 'Pagos de venta'

    def __str__(self):
        return f"Pago #{self.id} - Monto: {self.monto}"

class PagoCompra(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(decimal_places=2, max_digits=12)
    nota = models.TextField(blank=True,null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name='pagos'
    )
    metodo_pago = models.ForeignKey(
        MedioPago,
        on_delete=models.PROTECT
    )
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='pagos_compra_registrados'
    )

    class Meta:
        indexes = [
            models.Index(fields=['orden_compra','-fecha']),
        ]
        ordering = ['-fecha']
        verbose_name = 'Pago de compra'
        verbose_name_plural = 'Pagos de compra'
    
    def clean(self):
        if self.monto <= 0:
            raise ValidationError("El monto debe ser mayor a cero")
        
        if self.monto > self.orden_compra.saldo_pendiente:
            raise ValidationError(f"El pago excede el saldo pendiente: ${self.orden_compra.saldo_pendiente}")
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pago #{self.id} - Monto: {self.monto}"
