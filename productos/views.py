from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto, Marca
from .serializers import ProductoSerializer, MarcaSerializer
from .permissions import PermitirTodo
from rest_framework import viewsets
# Create your views here.

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [PermitirTodo]
    
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [PermitirTodo]

