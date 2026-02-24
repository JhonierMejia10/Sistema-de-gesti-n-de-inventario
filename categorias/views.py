from rest_framework import viewsets
from .models import Categoria
from .serializers import CategoriaSerializer
from .permissions import PermitirTodo
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]    

