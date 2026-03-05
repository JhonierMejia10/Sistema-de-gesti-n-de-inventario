from django.db import models


# Create your models here.
class Almacen(models.Model):
    nombre = models.CharField(max_length=255, blank=False, null=False, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre