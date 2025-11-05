from django.db import models
from productos.models import Producto

# Create your models here.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre
    

class EstadoCompra(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class OrdenCompra(models.Model):
    fecha_orden = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=3)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE
    )
    estado = models.ForeignKey(
        EstadoCompra,
        on_delete=models.CASCADE
    )
    nota = models.TextField(blank=True, null=True)

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