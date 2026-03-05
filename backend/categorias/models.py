from django.db import models
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.descripcion is None or self.descripcion.strip() == "":
            return f"Categoria: {self.nombre} - Sin descripción"
        return f"Categoria: {self.nombre} - Descripción: {self.descripcion}"
    
