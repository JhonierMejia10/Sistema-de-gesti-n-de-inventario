from django.contrib import admin
from .models import Sitio,Almacen

# Register your models here.
admin.site.site_header = "Adminisración de almacenes"
admin.site.register(Sitio)
admin.site.register(Almacen)
