from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Producto
from inventario.models import Stock