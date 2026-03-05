from rest_framework import viewsets
from .models import Stock, Movimiento
from .serializers import StockSerializer, MovimientoSerializer

from rest_framework.permissions import IsAuthenticated

# Create your views here.

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.select_related('producto', 'almacen').all()
    serializer_class = StockSerializer
    search_fields = ['id', 'producto__nombre', 'almacen__nombre']
    permission_classes = [IsAuthenticated]
    
class MovimientoViewSetOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    search_fields = ['id', 'producto__nombre', 'tipo_movimiento']
    permission_classes = [IsAuthenticated]

    
