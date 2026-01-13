from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from .models import Orden, OrdenItem
from inventario.models import Movimiento, Stock
from pagos.models import PagoVenta
from django.db.models import Sum

class OrdenVentaService:

    @staticmethod
    @transaction.atomic
    def agregar_al_carrito(usuario_creador, cliente_id, almacen, producto, cantidad, precio_unitario):

       return 1