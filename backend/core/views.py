from rest_framework import viewsets
from .models import EstadoPago
from .serializers import EstadoPagoSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from productos.models import Producto
from ventas.models import Orden
from compras.models import OrdenCompra


class EstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer
    permission_classes = [IsAuthenticated]

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = {
            "total_productos": Producto.objects.filter(activo=True).count(),
            "total_ventas": Orden.objects.count(),
            "compras_pendientes": OrdenCompra.objects.filter(
                estado_compra=OrdenCompra.EstadoCompraChoices.PENDIENTE
            ).count(),
        }
        return Response(stats)

