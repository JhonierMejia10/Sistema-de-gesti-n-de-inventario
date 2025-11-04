from django.shortcuts import render
from .models import Cliente, TipoCliente
from .serializers import ClienteSerializer
from rest_framework import viewsets


# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]

class TipoClienteViewSet(viewsets.ModelViewSet):
    queryset = TipoCliente.objects.all()
    serializer_class = ClienteSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]