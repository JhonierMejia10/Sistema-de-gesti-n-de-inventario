from django.db import models
from ventas.models import Orden
from productos.models import Producto

# Create your models here.
class EstadoPedido(models.Model):
    nombre = models.CharField(max_length=100, unique=True, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    

class Pedido(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.CharField(max_length=255)
    observaciones = models.TextField(blank=True, null=True)
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    estado = models.ForeignKey(
        EstadoPedido,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Pedido #{self.id} - Orden #{self.orden.id}"
    
class PedidoItem(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField()