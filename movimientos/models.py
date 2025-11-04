from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User

# Create your models here.

class TipoMovimiento(models.Model):
    nombre = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE, null=True
    )
    tipo_movimiento = models.ForeignKey(
        TipoMovimiento,
        on_delete=models.CASCADE,
        null=False
    )
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.id


class MovimientoItem(models.Model):
    movimiento = models.ForeignKey(
        Movimiento,
        on_delete=models.CASCADE,
        related_name='tems'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad})"


    


