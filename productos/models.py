from django.db import models
from categorias.models import Categoria
from compras.models import Proveedor

# Create your models here.

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255, db_index=True, null=False)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=3, null=False)
    stock = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
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
    marca = models.ForeignKey(
        Marca,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    tipo_producto = models.ForeignKey(
        TipoProducto,
        on_delete=models.CASCADE
    )
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class TipoAtributoProducto(models.Model):
    nombre = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.nombre


class AtributoProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    tipo_atributo = models.ForeignKey(
        TipoAtributoProducto,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.producto.nombre} - {self.tipo_atributo.nombre}"

class ValorAtributoProducto(models.Model):
    atributo_producto = models.ForeignKey(
        AtributoProducto,
        on_delete=models.CASCADE
    )
    valor = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.atributo_producto.tipo_atributo.nombre}: {self.valor}"

