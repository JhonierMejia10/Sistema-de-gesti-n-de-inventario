from django.db import models
from django.utils.text import slugify

# Create your models here.


class TipoCliente(models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.nombre} : {self.descripcion}"
    
class Cliente(models.Model):
    tipo_cliente = models.ForeignKey(
        TipoCliente,
        on_delete=models.CASCADE,
        related_name='clientes'
    )
    nombre = models.CharField(max_length=100, blank=False ,null=False)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    nit = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.nombre
