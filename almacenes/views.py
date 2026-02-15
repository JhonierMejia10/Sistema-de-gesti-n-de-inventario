from .models import Ubicacion, Almacen
from .serializers import UbicacionSerializer, AlmacenSerializer
from .permissions import PermitirTodo
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer
    permission_classes = [IsAuthenticated]
    
class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]