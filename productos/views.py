from django.shortcuts import render
from rest_framework.response import Response
from .models import TipoProducto, Marca, Producto, TipoAtributoProducto, AtributoProducto
from .serializers import TipoProductoSerializer, MarcaSerializer ,CrearProductoSerializer , ProductoSerializer, TipoAtrubutoProductoSerializer, AtributoProductoSerializer
from .permissions import PermitirTodo
from .services import ProductosService
from rest_framework import viewsets, status
from rest_framework.views import APIView
# Create your views here.


class TipoProductoViewSet(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    permission_classes = [PermitirTodo]

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [PermitirTodo]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [PermitirTodo]

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
                descripcion=data["descripcion"],
                precio=data["precio"],
                foto=data["foto"],
                categoria=data["categoria"],
                marca=data["marca"],
                tipo_producto=data["tipo_producto"],
                nota=data["nota"]
            )
        except Exception as e:
            return Response(
                {'error':str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"mensaje":"Producto creado exitosamente.",
             "producto":{producto.nombre},
            "precio":{producto.precio},
            "tipo_producto":{producto.tipo_producto},
            "categoria":{producto.categoria}
             }, status=status.HTTP_201_CREATED
        )

