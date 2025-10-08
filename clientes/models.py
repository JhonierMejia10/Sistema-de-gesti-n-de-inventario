from django.db import models

# Create your models here.
class Cliente(models.Model):
    Tipos_clientes = [
        ("per","Persona"),
        ("Emp","Empresa"),
        ("Anon","Anónimo")
    ]

    nombre = models.CharField(max_length=100)
    tipo_cliente = models.CharField(choices=Tipos_clientes, db_index=True, max_length=10)
    contacto = models.CharField(max_length=50, null=True, blank=True)
    nit = models.IntegerField(null=True, blank=True)
