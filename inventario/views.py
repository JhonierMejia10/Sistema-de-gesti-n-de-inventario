from rest_framework import viewsets
from .models import Stock, TipoMovimiento, Movimiento
from .serializers import StockSerializer, TipoMovimientoSerializer ,MovimientoSerializer
from .permissions import PermitirTodo

from rest_framework.permissions import IsAuthenticated

# Create your views here.

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    
class TipoMovimientoViewSet(viewsets.ModelViewSet):
    queryset = TipoMovimiento.objects.all()
    serializer_class = TipoMovimientoSerializer
    permission_classes = [IsAuthenticated]

class MovimientoViewSetOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]

    
