from django.shortcuts import render
from .models import Pago, MedioPago, EstadoPago
from .serializers import PagoSerializer, MedioPagoSerializer, EstadoPagoSerializer
from rest_framework import viewsets
# Create your views here.


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class MedioPagoViewSet(viewsets.ModelViewSet):
    queryset = MedioPago.objects.all()
    serializer_class = MedioPagoSerializer  

class EstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer





