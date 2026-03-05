from django.db import models
from ventas.models import Orden

# Create your models here.
class Pedido(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.CharField(max_length=255)
    observaciones = models.TextField(blank=True, null=True)
    class EstadoPedidoChoices(models.TextChoices):
        PREPARANDO = 'Preparando', 'Preparando'
        ENVIADO = 'Enviado', 'Enviado'
        ENTREGADO = 'Entregado', 'Entregado'
        CANCELADO = 'Cancelado', 'Cancelado'

    orden = models.OneToOneField(
        Orden,
        on_delete=models.CASCADE,
        related_name='pedido'
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoPedidoChoices.choices,
        default=EstadoPedidoChoices.PREPARANDO,
        db_index=True
    )

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Pedido #{self.id} - Orden #{self.orden.id}"