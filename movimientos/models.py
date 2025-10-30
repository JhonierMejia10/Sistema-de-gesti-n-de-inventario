from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User

# Create your models here.
class Movimiento(models.Model):
    
    tipo_movimiento_list = [
        ("Entrada","Entrada"),
        ("Orden de venta","Orden de venta"),
        ("Ajuste","Ajuste")
    ]

    tipo_movimiento = models.CharField(choices=tipo_movimiento_list, db_index=True, max_length=15)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE, null=True
    )
    nota = models.TextField(blank=True, null=True)


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


    


