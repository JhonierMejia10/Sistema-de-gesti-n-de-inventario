from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Categoria
from .serializers import CategoriaSerializer
# Create your views here.

def vistaprueba(request):
    return JsonResponse({'message':"Vista de categorias funcionando correctamente"})

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    

