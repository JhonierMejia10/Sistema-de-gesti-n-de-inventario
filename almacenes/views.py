from django.shortcuts import render
from .models import Sitio, Almacen
from .serializers import SitioSerializer, AlmacenSerializer
from rest_framework import viewsets

# Create your views here.

class SitioViewSet(viewsets.ModelViewSet):
    queryset = Sitio.objects.all()
    serializer_class = SitioSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    
class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    lookup_field = 'slug'