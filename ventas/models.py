from django.db import models
from clientes.models import Cliente
from productos.models import Producto
from django.contrib.auth.models import User

# Create your models here.

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
    precio_unitario = models.DecimalField(decimal_places=3, max_digits=10)
    precio = models.DecimalField(decimal_places=3, max_digits=10)

    class Meta:
        unique_together = ('producto','cliente')
    

class Orden(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ordenes_creadas'
    )
    total = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    fecha = models.DateField(db_index=True, auto_now_add=True)
    


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
    precio = models.DecimalField(max_digits=10, decimal_places=3)

    #Restricción para que se cree una sola instancia de producto por cada orden
    class Meta:
        unique_together = ('orden','producto')


