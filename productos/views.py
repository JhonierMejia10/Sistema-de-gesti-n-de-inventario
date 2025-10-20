from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework import viewsets
# Create your views here.


def vistaprueba(request):
    return JsonResponse({'message':"Vista de productos funcionando correctamente"})

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    