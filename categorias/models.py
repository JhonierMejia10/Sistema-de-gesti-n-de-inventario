from django.db import models
from django.utils.text import slugify
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    #Se reescribió el método save para crear y guardar automáticamente los slugs usando la clase slugify
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.descripcion is None or self.descripcion.strip() == "":
            return f"Categoria: {self.nombre} - Sin descripción"
        return f"Categoria: {self.nombre} - Descripción: {self.descripcion}"
    
