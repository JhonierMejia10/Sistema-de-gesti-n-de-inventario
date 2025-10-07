from django.db import models
from ..categorias.models import categoria
from ..proveedores.models import proveedor


# Create your models here.
class producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField()
    stock = models.IntegerField()
    fecha_creacion = models.DateTimeField()
    categoria = models.ForeignKey(
        categoria,
        on_delete=models.CASCADE
    )
    proveedor = models.ForeignKey(
        proveedor,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.nombre



