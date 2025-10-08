from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(default=None, max_length=100)
    telefono = models.CharField(max_length=20)