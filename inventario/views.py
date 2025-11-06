from rest_framework import viewsets
from .models import Stock, TipoMovimiento, Movimiento, MovimientoItem
from .serializers import StockSerializer, TipoMovimientoSerializer ,MovimientoSerializer, MovimientoItemSerializer 

# Create your views here.

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    
class TipoMovimientoViewSet(viewsets.ModelViewSet):
    queryset = TipoMovimiento
    serializer_class = TipoMovimientoSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]

class MovimientoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    

class MovimientoItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MovimientoItem.objects.all()
    serializer_class = MovimientoItemSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    
