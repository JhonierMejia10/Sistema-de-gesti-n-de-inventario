from django.shortcuts import render
from .models import Cliente
from .serializers import ClienteSerializer
from rest_framework import viewsets


# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
