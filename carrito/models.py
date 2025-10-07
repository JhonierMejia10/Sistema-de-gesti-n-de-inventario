from django.db import models
from ..clientes.models import cliente
from ..productos.models import producto

# Create your models here.

class Carrito(models.Model):
    cliente = models.ForeignKey(
        cliente,
        on_delete=models.CASCADE
    )
    producto = models.ForeignKey(
        producto,
        on_delete=models.CASCADE
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField()
    precio = models.DecimalField()

    class Meta:
        unique_together = ('producto','cliente')
    