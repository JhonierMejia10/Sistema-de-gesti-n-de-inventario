from django.db import models
from categorias.models import Categoria
from proveedores.models import Proveedor


# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=255, db_index=True, null=False)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    stock = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )
    proveedor = models.ForeignKey(
        Proveedor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.nombre



