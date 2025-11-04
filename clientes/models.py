from django.db import models

# Create your models here.


class TipoCliente(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    Tipos_cliente = models.ForeignKey(
        TipoCliente,
        on_delete=models.CASCADE,
        related_name='clientes'

    )
    nombre = models.CharField(max_length=100, null=False)
    contacto = models.CharField(max_length=50, null=True, blank=True)
    nit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre
