from django.shortcuts import render
from rest_framework import viewsets
from .models import EstadoPago
from .serializers import EstadoPagoSerializer
from .permissions import PermitirTodo
# Create your views here.

class EstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer
    permission_classes = [PermitirTodo]
