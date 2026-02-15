from rest_framework import viewsets
from .models import Categoria
from .serializers import CategoriaSerializer
from .permissions import PermitirTodo
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]    

