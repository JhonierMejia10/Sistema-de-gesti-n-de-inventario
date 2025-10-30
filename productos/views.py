from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto, Marca
from .serializers import ProductoSerializer, MarcaSerializer
from rest_framework import viewsets
# Create your views here.



class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

    def get_permissions(self):
        permission_casses = []
        return [permission() for permission in permission_casses]