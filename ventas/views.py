from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import CarritoSerializer, OrdenSerializer, OrdenItemSerializer
from .models import Carrito, Orden, OrdenItem
from rest_framework.response import Response


# Create your views here.

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
        
    def get_queryset(self):
        cliente_id = self.request.query_params.get('cliente')
        if cliente_id:
            return Carrito.objects.filter(cliente_id=cliente_id)
        return Carrito.objects.none()
    
    def delete(self, request, *args, **kwarteags):
        Carrito.objects.filter(cliente_id=request.query_params.get('cliente')).delete()
        return Response("Oks")