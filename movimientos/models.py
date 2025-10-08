from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User

# Create your models here.
class MovimientoInventario(models.Model):
    
    #Tipos de movimientos disponibles, se definió una lista con tuplas en primera instancia
    tipo_movimiento_list = [
        ("In","Entrada"),
        ("Vent","Orden de venta"),
        ("Adj","Ajuste")
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    tipo_movimiento = models.CharField(choices=tipo_movimiento_list, db_index=True, max_length=4)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, null=True
    )
    nota = models.TextField(blank=True, null=True)

    


