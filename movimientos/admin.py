from django.contrib import admin
from .models import Movimiento, TipoMovimiento
# Register your models here.
admin.site.register(Movimiento)
admin.site.register(TipoMovimiento)