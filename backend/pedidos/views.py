from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Pedido
from .serializers import PedidoSerializer, ActualizarPedidoSerializer



class PedidoViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    Pedidos: solo listar, ver detalle y actualizar estado.
    No se permite crear ni eliminar manualmente (se crean desde ventas).
    """
    queryset = Pedido.objects.select_related(
        'orden', 'orden__cliente'
    ).order_by('-fecha_creacion')
    search_fields = ['id', 'orden__id', 'orden__cliente__nombre']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ActualizarPedidoSerializer
        return PedidoSerializer

    def update(self, request, *args, **kwargs):
        return self._handle_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._handle_update(request, *args, **kwargs)

    def _handle_update(self, request, *args, **kwargs):
        from .services import PedidoService
        from django.core.exceptions import ValidationError as DjangoValidationError
        from rest_framework.exceptions import ValidationError as DRFValidationError

        pedido = self.get_object()
        serializer = ActualizarPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            pedido_actualizado = PedidoService.actualizar_pedido_service(
                pedido_id=pedido.id,
                nuevo_estado=data['estado'],
                observaciones=data.get('observaciones'),
                usuario_modificador=request.user
            )
        except DjangoValidationError as e:
            raise DRFValidationError(e.message)

        return Response(PedidoSerializer(pedido_actualizado).data, status=status.HTTP_200_OK)
