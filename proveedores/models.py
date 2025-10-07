from django.db import models

# Create your models here.
class proveedor(models.Model):
    nombre = models.CharField()
    contacto = models.CharField(default=None)
    telefono = models.CharField()