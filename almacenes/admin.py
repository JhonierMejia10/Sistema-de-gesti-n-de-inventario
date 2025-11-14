from django.contrib import admin
from .models import Ubicacion,Almacen

# Register your models here.
admin.site.site_header = "Adminisración de almacenes"
admin.site.register(Ubicacion)
admin.site.register(Almacen)
