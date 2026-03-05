from .models import Almacen
from .serializers import AlmacenSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import ProtectedError

# Create your views here.


class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    search_fields = ['id', 'nombre', 'direccion']
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {"detail": f"No se puede eliminar el almacén '{instance.nombre}' porque tiene órdenes de venta o compra asociadas. Elimina o reasigna esas órdenes primero."},
                status=status.HTTP_409_CONFLICT
            )