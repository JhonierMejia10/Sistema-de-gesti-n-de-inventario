from .models import Cliente
from .serializers import ClienteSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    search_fields = ['id', 'nombre', 'nit', 'correo']
    permission_classes = [IsAuthenticated]