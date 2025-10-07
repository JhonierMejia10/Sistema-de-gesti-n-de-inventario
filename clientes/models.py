from django.db import models

# Create your models here.
class cliente(models.Model):
    Tipos_clientes = [
        ("per","Persona"),
        ("Emp","Empresa"),
        ("Anon","Anónimo")
    ]

    nombre = models.CharField(max_length=100)
    tipo_cliente = models.CharField(choices=Tipos_clientes, db_index=True)
    contacto = models.CharField(max_length=50)
