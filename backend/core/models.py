from django.db import models


# Create your models here.
class EstadoPago(models.Model):
    nombre = models.CharField(max_length=255, blank=False, null=False, unique=True)
    descripcion = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name_plural = "Estados de pago"
        ordering = ['nombre']
    
    @classmethod
    def obtener_pendiente(cls):
        """Caché del estado Pendiente"""
        if not hasattr(cls, '_pendiente'):
            cls._pendiente = cls.objects.get(nombre='Pendiente')
        return cls._pendiente
    
    @classmethod
    def obtener_abonado(cls):
        """Caché del estado Abonado"""
        if not hasattr(cls, '_abonado'):
            cls._abonado = cls.objects.get(nombre='Abonado')
        return cls._abonado
    
    @classmethod
    def obtener_completado(cls):
        """Caché del estado Completado"""
        if not hasattr(cls, '_completado'):
            cls._completado = cls.objects.get(nombre='Completado')
        return cls._completado

    def __str__(self):
        if self.descripcion is None or self.descripcion.strip() == "":
            return f"Estado de pago: {self.nombre} - Sin descripción"
        return f"Estado de pago: {self.nombre} - Descripción: {self.descripcion}"

from decimal import Decimal

class TransaccionBase(models.Model):
    """
    Clase base abstracta para transacciones como OrdenCompra y Orden de Venta.
    Centraliza todos los calculos pendientes y de estados de pago
    en base a los campos físicos de la base de datos (total y total_pagado).
    """
    total = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    total_pagado = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    class Meta:
        abstract = True
        
    @property
    def saldo_pendiente(self):
        return self.total - self.total_pagado

    @property
    def estado_pago_calculado(self):
        """
        Calcula el estado dinámicamente. 
        El servicio es responsable de evaluar esto y guardarlo en el campo fk estado_pago.
        """
        if self.total_pagado == Decimal('0'):
            return EstadoPago.obtener_pendiente()
        elif self.total_pagado >= self.total:
            return EstadoPago.obtener_completado()
        else:
            return EstadoPago.obtener_abonado()
