from rest_framework.response import Response
from .models import Marca, Producto
from .serializers import MarcaSerializer ,CrearProductoSerializer , ProductoSerializer
from .services import ProductosService
from rest_framework import viewsets, status

from rest_framework.permissions import IsAuthenticated

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    search_fields = ['id', 'nombre', 'descripcion']
    permission_classes = [IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.prefetch_related('stock_set', 'stock_set__almacen').all()
    serializer_class = ProductoSerializer
    search_fields = ['id', 'nombre', 'descripcion']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CrearProductoSerializer
        return ProductoSerializer

    def create(self, request):
        serializer = CrearProductoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            producto = ProductosService.crear_producto_service(
                nombre=data["nombre"],
                descripcion=data.get("descripcion"),
                precio=data["precio"],
                foto=data.get("foto"),
                categoria=data["categoria"],
                marca=data.get("marca"),
                tipo_producto=data["tipo_producto"],
                nota=data.get("nota"),
                stock_inicial=data["stock_inicial"],
                almacen=data["almacen"]
            )
        except Exception as e:
            return Response(
                {'error':str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        producto_serializer = ProductoSerializer(producto)
        return Response(producto_serializer.data, status=status.HTTP_201_CREATED)

