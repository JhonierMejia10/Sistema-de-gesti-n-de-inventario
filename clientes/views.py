from django.shortcuts import render
from .models import Cliente, TipoCliente
from .serializers import ClienteSerializer, TipoClienteSerializer
from .permissions import PermitirTodo
from rest_framework import viewsets


# Create your views here.

class TipoClienteViewSet(viewsets.ModelViewSet):
    queryset = TipoCliente.objects.all()
    serializer_class = TipoClienteSerializer
    lookup_field = 'slug'
    permission_classes = [PermitirTodo]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [PermitirTodo]