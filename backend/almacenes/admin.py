from django.contrib import admin
from .models import Almacen

# Register your models here.
admin.site.site_header = "Adminisración de almacenes"
admin.site.register(Almacen)
