from django.contrib import admin
from .models import Movimiento, TipoMovimiento, MovimientoItem
# Register your models here.
admin.site.register(Movimiento)
admin.site.register(TipoMovimiento)
admin.site.register(MovimientoItem)