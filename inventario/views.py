from rest_framework import viewsets
from .models import Stock, TipoMovimiento, Movimiento, MovimientoItem
from .serializers import StockSerializer, TipoMovimientoSerializer ,MovimientoSerializer, MovimientoItemSerializer 
from .permissions import PermitirTodo

# Create your views here.

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [PermitirTodo]
    
class TipoMovimientoViewSet(viewsets.ModelViewSet):
    queryset = TipoMovimiento.objects.all()
    serializer_class = TipoMovimientoSerializer
    permission_classes = [PermitirTodo]

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [PermitirTodo]
    
class MovimientoItemViewSet(viewsets.ModelViewSet):
    queryset = MovimientoItem.objects.all()
    serializer_class = MovimientoItemSerializer
    permission_classes = [PermitirTodo]
    
