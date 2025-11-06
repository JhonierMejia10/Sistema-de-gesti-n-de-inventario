from django.db import models
from productos.models import Producto, ValorAtributoProducto
from almacenes.models import Almacen
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
    )
    almacen = models.ForeignKey(
        Almacen,
        on_delete=models.CASCADE
    )
    cantidad_en_mano = models.IntegerField()
    valor_atributo_producto = models.ForeignKey(
        ValorAtributoProducto,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Producto: {self.producto.nombre} - Almacen: {self.almacen.nombre_almacen} - Cantidad: {self.cantidad_en_mano} unidades"

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
        return f"Movimiento {self.id} - Tipo: {self.tipo_movimiento.nombre} - Fecha: {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"



class MovimientoItem(models.Model):
    movimiento = models.ForeignKey(
        Movimiento,
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad})"


