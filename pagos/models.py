
from django.db import models
from ventas .models import Orden

# Create your models here.
class EstadoPago(models.Model):
    nombre = models.CharField(max_length=100, db_index=True, null=False, blank=False)
    
    def __str__(self):
        return self.nombre
    

class Pago(models.Model):
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        db_index=True
    )
    estado_pago = models.ForeignKey(
        EstadoPago,
        on_delete=models.PROTECT
    )
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(decimal_places=3, max_digits=65)

    def __str__(self):
        return self.id

class MedioPago(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

