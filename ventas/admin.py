from django.contrib import admin
from .models import Orden,OrdenItem,Carrito,EstadoPago

# Register your models here.
admin.site.register(OrdenItem)
admin.site.register(Orden)
admin.site.register(Carrito)
admin.site.register(EstadoPago)