from django.db import models

# Create your models here.
class Sitio(models.Model):
    pais = models.CharField(max_length=70, default='Colombia', blank=True, null=True)
    ciudad = models.CharField(max_length=100, default='Medellín', blank=True, null=True)
    barrio = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

class Almacen(models.Model):
    nombre_almacen = models.CharField(max_length=255, blank=True, null=True)
    sitio = models.ForeignKey(
        Sitio,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)