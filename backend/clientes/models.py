from django.db import models

# Create your models here.


class Cliente(models.Model):
    class TipoClienteChoices(models.TextChoices):
        NATURAL = 'Persona Natural', 'Persona Natural'
        JURIDICA = 'Persona Jurídica', 'Persona Jurídica'

    tipo_cliente = models.CharField(
        max_length=20,
        choices=TipoClienteChoices.choices,
        default=TipoClienteChoices.NATURAL,
        db_index=True
    )
    nombre = models.CharField(max_length=100, blank=False ,null=False)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    nit = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.nombre
