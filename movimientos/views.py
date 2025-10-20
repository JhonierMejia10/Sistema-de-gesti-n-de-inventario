from django.shortcuts import render
from rest_framework import viewsets
from .models import MovimientoInventario
from .serializers import MovimientoSerializer
from rest_framework.permissions import IsAdminUser

# Create your views here.

class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]