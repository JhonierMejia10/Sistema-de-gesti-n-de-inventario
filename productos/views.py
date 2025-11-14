from django.shortcuts import render
from django.http import JsonResponse
from .models import TipoProducto, Marca, Producto, TipoAtributoProducto, AtributoProducto
from .serializers import TipoProductoSerializer, MarcaSerializer , ProductoSerializer, TipoAtrubutoProductoSerializer, AtributoProductoSerializer
from .permissions import PermitirTodo
from rest_framework import viewsets
# Create your views here.


class TipoProductoViewSet(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    permission_classes = [PermitirTodo]

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [PermitirTodo]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [PermitirTodo]
    