from django.db import models
from productos.models import Producto
from almacenes.models import Almacen
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Stock(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    almacen = models.ForeignKey(
        Almacen,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    cantidad_en_mano = models.PositiveIntegerField(blank=False,null=False)

    class Meta:
        unique_together = ['producto','almacen']

    def __str__(self):
        return f"Producto: {self.producto.nombre} - Almacen: {self.almacen.nombre} - Cantidad: {self.cantidad_en_mano} unidades"


    
class Movimiento(models.Model):
    class TipoMovimientoChoices(models.TextChoices):
        ENTRADA = 'ENTRADA', 'Entrada'
        SALIDA = 'SALIDA', 'Salida'

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE, null=True,
        related_name='movimientos_inventario'
    )
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=TipoMovimientoChoices.choices,
        db_index=True
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    almacen = models.ForeignKey(
        Almacen,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    cantidad = models.PositiveIntegerField()

    saldo_anterior = models.IntegerField()
    saldo_nuevo= models.IntegerField()

    #Relación al documento fuente
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    referencia = GenericForeignKey('content_type','object_id')
    nota = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['producto','-fecha_creacion']),
            models.Index(fields=['tipo_movimiento','-fecha_creacion']),
            models.Index(fields=['almacen','-fecha_creacion']),
        ]
        verbose_name = 'Movimiento de inventario'
        verbose_name_plural = 'Movimientos de inventario'

    def __str__(self):
        return f"Movimiento {self.id} - Tipo: {self.tipo_movimiento} - Fecha: {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"

