from django.db import models

# Create your models here.


class TipoCliente(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    tipo_cliente = models.ForeignKey(
        TipoCliente,
        on_delete=models.CASCADE,
        related_name='clientes'

    )
    nombre = models.CharField(max_length=100, null=False)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    nit = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.nombre
