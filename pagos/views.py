from rest_framework import viewsets
from .models import  MedioPago, PagoVenta, PagoCompra
from .serializers import MedioPagoSerializer,  PagoVentaSerializer
from .permissions import PermitirTodo

# Create your views here.


class PagoViewSet(viewsets.ModelViewSet):
    queryset = PagoVenta.objects.all()
    serializer_class = PagoVentaSerializer
    permission_classes = [PermitirTodo]

class MedioPagoViewSet(viewsets.ModelViewSet):
    queryset = MedioPago.objects.all()
    serializer_class = MedioPagoSerializer
    permission_classes = [PermitirTodo]  





