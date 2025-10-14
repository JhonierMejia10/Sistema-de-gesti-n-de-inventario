from django.db import models

# Create your models here.
class Cliente(models.Model):
    Tipos_clientes = [
        ("Persona","Persona"),
        ("Empresa","Empresa"),
        ("Anonimo","Anónimo")
    ]

    nombre = models.CharField(max_length=100, null=False)
    tipo_cliente = models.CharField(choices=Tipos_clientes, db_index=True, max_length=10, default='Anonimo')
    contacto = models.CharField(max_length=50, null=True, blank=True)
    nit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre
