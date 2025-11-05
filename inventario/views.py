from rest_framework import viewsets
from .models import Movimiento, MovimientoItem, TipoMovimiento
from .serializers import MovimientoSerializer, MovimientoItemSerializer, TipoMovimientoSerializer

# Create your views here.

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
    
class TipoMovimientoViewSet(viewsets.ModelViewSet):
    queryset = TipoMovimiento
    serializer_class = TipoMovimientoSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]