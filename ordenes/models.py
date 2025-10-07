from django.db import models
from ..clientes.models import cliente
from ..productos.models import producto

# Create your models here.
class orden(models.Model):
    estados = [
        ("Pen","Pendiente"),
        ("Abon","Abono"),
        ("Can","Cancelado")
    ]

    cliente = models.ForeignKey(
        cliente
    )
    estado_pago = models.CharField(choices=estados, db_index=True)
    total = models.DecimalField(default=0)
    fecha = models.DateField(db_index=True)

class ordenItem(models.Model):
    orden = models.ForeignKey(
        orden,
        on_delete=models.CASCADE,
        related_name='orden'
    )
    producto = models.ForeignKey(
        producto,
        on_delete=models.CASCADE
    )
    cantidad = models.IntegerField()
    precio = models.DecimalField()

    #Restricción para que se cree una sola instancia de producto por cada orden
    class Meta:
        unique_together = ('orden','producto')