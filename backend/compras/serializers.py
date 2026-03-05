from rest_framework import serializers
from .models import Proveedor, OrdenCompra, ItemOrdenCompra
from productos.models import Producto
from almacenes.models import Almacen
from pagos.models import MedioPago

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ItemOrdenCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrdenCompra
        fields = ["orden_compra","id", "producto", "cantidad", "precio_unitario"]
        read_only_fields = ['orden_compra']
    

class OrdenCompraSerializer(serializers.ModelSerializer):
    items = ItemOrdenCompraSerializer(many=True, required=False)
    total_pagado = serializers.SerializerMethodField()
    saldo_pendiente = serializers.SerializerMethodField()
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)

    class Meta:
        model = OrdenCompra
        fields = "__all__"

    def get_total_pagado(self, obj):
        return obj.total_pagado

    def get_saldo_pendiente(self, obj):
        return obj.saldo_pendiente

"""Serializers usados para la creación de una orden de comora"""
class ItemCompraSerializer(serializers.Serializer):
    producto = serializers.PrimaryKeyRelatedField(
        queryset = Producto.objects.all()
    )
    cantidad = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )

class CrearCompraSerializer(serializers.Serializer):
    ubicacion_entrega = serializers.PrimaryKeyRelatedField(
        queryset = Almacen.objects.all()
    )
    proveedor = serializers.PrimaryKeyRelatedField(
        queryset = Proveedor.objects.all()
    )
    estado_compra = serializers.ChoiceField(
        choices=OrdenCompra.EstadoCompraChoices.choices
    )
    pago_inicial = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, default=0)
    metodo_pago = serializers.PrimaryKeyRelatedField(
        queryset = MedioPago.objects.all(),
        required = False,
        allow_null = True
    )
    items = ItemCompraSerializer(many=True)
    nota = serializers.CharField(required=False, allow_null=True)
    fecha_esperada = serializers.DateField(required=False, allow_null=True)

class ActualizarCompraSerializer(serializers.Serializer):
    """Serializer para actualizar estado logístico y nota de una orden de compra"""
    estado_compra = serializers.ChoiceField(
        choices=OrdenCompra.EstadoCompraChoices.choices
    )
    nota = serializers.CharField(required=False, allow_null=True, allow_blank=True)
