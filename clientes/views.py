from django.shortcuts import render
from .models import Cliente, TipoCliente
from .serializers import ClienteSerializer, TipoClienteSerializer
from .permissions import PermitirTodo
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class TipoClienteViewSet(viewsets.ModelViewSet):
    queryset = TipoCliente.objects.all()
    serializer_class = TipoClienteSerializer
    permission_classes = [IsAuthenticated]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]