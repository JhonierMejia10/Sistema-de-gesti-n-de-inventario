from django.shortcuts import render
from .models import Proveedor
from .serializers import ProveedorSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

# Create your views here.

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]