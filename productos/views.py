from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework import viewsets
# Create your views here.



class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    