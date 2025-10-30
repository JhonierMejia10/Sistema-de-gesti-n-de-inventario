from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Categoria
from .serializers import CategoriaSerializer
# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]    

