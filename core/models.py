from django.db import models
from django.utils.text import slugify

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