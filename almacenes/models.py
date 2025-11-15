from django.db import models
from django.utils.text import slugify

# Create your models here.
class Ubicacion(models.Model):
    pais = models.CharField(max_length=70, default='Colombia')
    ciudad = models.CharField(max_length=100, default='Medellín', blank=True, null=True)
    barrio = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.ciudad} - {self.barrio} - {self.direccion}"

class Almacen(models.Model):
    nombre = models.CharField(max_length=255, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre