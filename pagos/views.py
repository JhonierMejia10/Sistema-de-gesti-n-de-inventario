from rest_framework import viewsets
from .models import Pago, MedioPago, EstadoPago
from .serializers import PagoSerializer, MedioPagoSerializer, EstadoPagoSerializer
from .permissions import PermitirTodo

# Create your views here.


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [PermitirTodo]

class MedioPagoViewSet(viewsets.ModelViewSet):
    queryset = MedioPago.objects.all()
    serializer_class = MedioPagoSerializer
    permission_classes = [PermitirTodo]  

class EstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer
    permission_classes = [PermitirTodo]





