from django.db import models
from categorias.models import Categoria


# Create your models here.

TIPO_PRODUCTO_CHOICES = [
    ('Bienes', 'Bienes'),
    ('Servicios', 'Servicios'),
]

class Marca(models.Model):
    nombre = models.CharField(max_length=255, unique=True, db_index=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255, db_index=True,blank=False, null=False, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )
    marca = models.ForeignKey(
        Marca,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    tipo_producto = models.CharField(
        max_length=20,
        choices=TIPO_PRODUCTO_CHOICES,
        default='Bienes'
    )
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

