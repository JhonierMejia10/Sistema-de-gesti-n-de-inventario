from django.db import models
from productos.models import Producto
from almacenes.models import Almacen
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - Telefono: {self.telefono} - Correo: {self.correo}"
    

class EstadoCompra(models.Model):
    nombre = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.nombre


class OrdenCompra(models.Model):
    fecha_orden = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=3)
    nota = models.TextField(blank=True, null=True)
    ubicacion_entrega = models.ForeignKey(
        Almacen,
        on_delete=models.CASCADE
    )
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE
    )
    estado = models.ForeignKey(
        EstadoCompra,
        on_delete=models.CASCADE
    )
    

    def __str__(self):
        return f"Orden de compra #{self.id} realizada al proveedor ({self.proveedor.nombre}) el día {self.fecha_orden.strftime('%Y-%m-%d')}" 
    

class ItemOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=3)
    
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} "