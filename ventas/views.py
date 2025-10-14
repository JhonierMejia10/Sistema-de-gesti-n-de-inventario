from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CarritoSerializer
from .models import Carrito

# Create your views here.

class CarritoListCreateAPIView(ListCreateAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
