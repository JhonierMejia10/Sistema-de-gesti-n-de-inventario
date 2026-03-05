"""
Tests unitarios para los servicios críticos del sistema de gestión de inventario.
Cubre: OrdenVentaService, CompraService, PagoService, ProductosService.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch

from almacenes.models import Almacen
from categorias.models import Categoria
from clientes.models import Cliente
from compras.models import OrdenCompra, Proveedor
from compras.services import CompraService
from core.models import EstadoPago
from inventario.models import Stock, Movimiento
from pagos.models import MedioPago, PagoVenta
from pagos.services import PagoService
from productos.models import Marca, Producto, TipoProducto
from productos.services import ProductosService
from ventas.models import Orden, OrdenItem
from ventas.services import OrdenVentaService
from django.core.exceptions import ValidationError


# ─────────────────────────────────────────────────────────────────
#  Helpers de fixtures
# ─────────────────────────────────────────────────────────────────

def crear_usuario():
    return User.objects.create_user(username='testuser', password='pass1234')


def crear_almacen():
    return Almacen.objects.create(nombre='Bodega Test', direccion='Colombia, Medellín')


def crear_producto(categoria, tipo_producto, precio=Decimal('100.00')):
    return Producto.objects.create(
        nombre=f'Producto Test {Producto.objects.count() + 1}',
        precio=precio,
        categoria=categoria,
        tipo_producto=tipo_producto,
    )


def crear_stock(producto, almacen, cantidad):
    return Stock.objects.create(
        producto=producto,
        almacen=almacen,
        cantidad_en_mano=cantidad
    )




def crear_estados_pago():
    pendiente, _ = EstadoPago.objects.get_or_create(id=1, defaults={'nombre': 'Pendiente'})
    abonado, _ = EstadoPago.objects.get_or_create(id=2, defaults={'nombre': 'Abonado'})
    completado, _ = EstadoPago.objects.get_or_create(id=3, defaults={'nombre': 'Completado'})
    return pendiente, abonado, completado


# ─────────────────────────────────────────────────────────────────
#  Tests: OrdenVentaService
# ─────────────────────────────────────────────────────────────────

class OrdenVentaServiceTest(TestCase):

    def setUp(self):
        self.usuario = crear_usuario()
        self.almacen = crear_almacen()

        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.tipo_producto = TipoProducto.objects.create(nombre='Físico')
        self.producto = crear_producto(self.categoria, self.tipo_producto)

        self.tipo_entrega = Orden.TipoEntregaChoices.CAJA

        self.pendiente, self.abonado, self.completado = crear_estados_pago()

        # Stock inicial: 10 unidades
        self.stock = crear_stock(self.producto, self.almacen, 10)

        self.cliente = Cliente.objects.create(
            nombre='Cliente Test',
            tipo_cliente=Cliente.TipoClienteChoices.NATURAL,
        )

    def _items_validos(self, cantidad=3):
        return [{'producto': self.producto, 'cantidad': cantidad, 'precio_unitario': Decimal('50.00')}]

    def test_crear_orden_venta_reduce_stock(self):
        """Crear una orden debe descontar el stock correctamente."""
        OrdenVentaService.crear_orden_venta_service(
            almacen=self.almacen,
            items=self._items_validos(cantidad=3),
            cliente=self.cliente,
            usuario_creador=self.usuario,
            tipo_entrega=self.tipo_entrega,
        )
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.cantidad_en_mano, 7)

    def test_crear_orden_registra_movimiento_salida(self):
        """Crear una orden debe registrar un movimiento de salida en inventario."""
        OrdenVentaService.crear_orden_venta_service(
            almacen=self.almacen,
            items=self._items_validos(cantidad=3),
            cliente=self.cliente,
            usuario_creador=self.usuario,
            tipo_entrega=self.tipo_entrega,
        )
        movimiento = Movimiento.objects.filter(producto=self.producto).first()
        self.assertIsNotNone(movimiento)
        self.assertEqual(movimiento.saldo_anterior, 10)
        self.assertEqual(movimiento.saldo_nuevo, 7)

    def test_venta_sin_stock_suficiente_lanza_error(self):
        """Pedir más unidades de las disponibles debe lanzar ValidationError."""
        with self.assertRaises(ValidationError):
            OrdenVentaService.crear_orden_venta_service(
                almacen=self.almacen,
                items=self._items_validos(cantidad=50),  # más de las 10 disponibles
                cliente=self.cliente,
                usuario_creador=self.usuario,
                tipo_entrega=self.tipo_entrega,
            )

    def test_venta_sin_stock_registrado_lanza_error(self):
        """Vender un producto sin ningún stock registrado debe fallar."""
        producto_sin_stock = crear_producto(self.categoria, self.tipo_producto)
        with self.assertRaises(ValidationError):
            OrdenVentaService.crear_orden_venta_service(
                almacen=self.almacen,
                items=[{'producto': producto_sin_stock, 'cantidad': 1, 'precio_unitario': Decimal('10.00')}],
                cliente=self.cliente,
                usuario_creador=self.usuario,
                tipo_entrega=self.tipo_entrega,
            )

    def test_orden_sin_items_lanza_error(self):
        """Crear una orden sin items debe fallar."""
        with self.assertRaises(ValidationError):
            OrdenVentaService.crear_orden_venta_service(
                almacen=self.almacen,
                items=[],
                cliente=self.cliente,
                usuario_creador=self.usuario,
                tipo_entrega=self.tipo_entrega,
            )

    def test_total_calculado_correctamente(self):
        """El total de la orden debe calcularse como suma de subtotales."""
        orden = OrdenVentaService.crear_orden_venta_service(
            almacen=self.almacen,
            items=[
                {'producto': self.producto, 'cantidad': 2, 'precio_unitario': Decimal('50.00')},
            ],
            cliente=self.cliente,
            usuario_creador=self.usuario,
            tipo_entrega=self.tipo_entrega,
        )
        self.assertEqual(orden.total, Decimal('100.00'))


# ─────────────────────────────────────────────────────────────────
#  Tests: PagoService
# ─────────────────────────────────────────────────────────────────

class PagoServiceTest(TestCase):

    def setUp(self):
        self.usuario = crear_usuario()
        self.almacen = crear_almacen()
        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.tipo_producto = TipoProducto.objects.create(nombre='Físico')
        self.producto = crear_producto(self.categoria, self.tipo_producto, precio=Decimal('100.00'))
        self.tipo_entrega = Orden.TipoEntregaChoices.ENVIO

        self.pendiente, self.abonado, self.completado = crear_estados_pago()
        crear_stock(self.producto, self.almacen, 20)

        self.cliente = Cliente.objects.create(nombre='Cliente', tipo_cliente=Cliente.TipoClienteChoices.NATURAL)

        self.orden = OrdenVentaService.crear_orden_venta_service(
            almacen=self.almacen,
            items=[{'producto': self.producto, 'cantidad': 1, 'precio_unitario': Decimal('100.00')}],
            cliente=self.cliente,
            usuario_creador=self.usuario,
            tipo_entrega=self.tipo_entrega,
            direccion_envio='Calle Test 123, Ciudad Test',
        )
        self.medio_pago = MedioPago.objects.create(nombre='Efectivo')

    def test_pago_parcial_deja_estado_abonado(self):
        """Un pago parcial debe actualizar el estado a Abonado."""
        PagoService.registrar_pago_venta(
            orden=self.orden,
            monto=Decimal('50.00'),
            metodo_pago=self.medio_pago,
            usuario=self.usuario,
        )
        self.orden.refresh_from_db()
        self.assertEqual(self.orden.estado_pago.nombre, 'Abonado')

    def test_pago_completo_deja_estado_completado(self):
        """Un pago por el total debe actualizar el estado a Completado."""
        PagoService.registrar_pago_venta(
            orden=self.orden,
            monto=Decimal('100.00'),
            metodo_pago=self.medio_pago,
            usuario=self.usuario,
        )
        self.orden.refresh_from_db()
        self.assertEqual(self.orden.estado_pago.nombre, 'Completado')

    def test_pago_que_excede_saldo_lanza_error(self):
        """Un pago que supera el saldo pendiente debe lanzar ValidationError."""
        with self.assertRaises(ValidationError):
            PagoService.registrar_pago_venta(
                orden=self.orden,
                monto=Decimal('999.00'),
                metodo_pago=self.medio_pago,
                usuario=self.usuario,
            )

    def test_pago_crea_registro_pagoventa(self):
        """Registrar un pago debe crear una instancia de PagoVenta."""
        pago = PagoService.registrar_pago_venta(
            orden=self.orden,
            monto=Decimal('50.00'),
            metodo_pago=self.medio_pago,
            usuario=self.usuario,
        )
        self.assertIsInstance(pago, PagoVenta)
        self.assertEqual(pago.monto, Decimal('50.00'))


# ─────────────────────────────────────────────────────────────────
#  Tests: ProductosService
# ─────────────────────────────────────────────────────────────────

class ProductosServiceTest(TestCase):

    def setUp(self):
        self.almacen = crear_almacen()
        self.categoria = Categoria.objects.create(nombre='Ropa')
        self.tipo_producto = TipoProducto.objects.create(nombre='Físico')

    def test_crear_producto_crea_stock_inicial(self):
        """Crear un producto debe crear automáticamente un registro de Stock."""
        producto = ProductosService.crear_producto_service(
            nombre='Camisa XL',
            precio=Decimal('45.00'),
            categoria=self.categoria,
            marca=None,
            tipo_producto=self.tipo_producto,
            stock_inicial=10,
            almacen=self.almacen,
        )
        stock = Stock.objects.filter(producto=producto, almacen=self.almacen).first()
        self.assertIsNotNone(stock)
        self.assertEqual(stock.cantidad_en_mano, 10)

    def test_crear_producto_con_stock_cero_es_valido(self):
        """Crear un producto con stock inicial 0 debe ser permitido."""
        producto = ProductosService.crear_producto_service(
            nombre='Producto Sin Stock',
            precio=Decimal('10.00'),
            categoria=self.categoria,
            marca=None,
            tipo_producto=self.tipo_producto,
            stock_inicial=0,
            almacen=self.almacen,
        )
        stock = Stock.objects.get(producto=producto, almacen=self.almacen)
        self.assertEqual(stock.cantidad_en_mano, 0)


# ─────────────────────────────────────────────────────────────────
#  Tests: CompraService
# ─────────────────────────────────────────────────────────────────

class CompraServiceTest(TestCase):

    def setUp(self):
        self.usuario = crear_usuario()
        self.almacen = crear_almacen()
        self.categoria = Categoria.objects.create(nombre='Herramientas')
        self.tipo_producto = TipoProducto.objects.create(nombre='Físico')
        self.producto = crear_producto(self.categoria, self.tipo_producto)
        self.proveedor = Proveedor.objects.create(nombre='Proveedor Test')
        self.pendiente, _, _ = crear_estados_pago()

        self.estado_pendiente = OrdenCompra.EstadoCompraChoices.PENDIENTE
        self.estado_recibido = OrdenCompra.EstadoCompraChoices.RECIBIDO

    def _items(self, cantidad=5):
        return [{'producto': self.producto, 'cantidad': cantidad, 'precio_unitario': Decimal('20.00')}]

    def test_crear_compra_pendiente_no_modifica_stock(self):
        """Una compra en estado Pendiente NO debe modificar el stock."""
        CompraService.crear_compra_service(
            ubicacion_entrega=self.almacen,
            proveedor=self.proveedor,
            estado_compra=self.estado_pendiente,
            items=self._items(cantidad=5),
            usuario_creador=self.usuario,
        )
        stock_count = Stock.objects.filter(producto=self.producto, almacen=self.almacen).count()
        self.assertEqual(stock_count, 0)

    def test_crear_compra_recibida_aumenta_stock(self):
        """Una compra en estado Recibido debe aumentar el stock del producto."""
        CompraService.crear_compra_service(
            ubicacion_entrega=self.almacen,
            proveedor=self.proveedor,
            estado_compra=self.estado_recibido,
            items=self._items(cantidad=5),
            usuario_creador=self.usuario,
        )
        stock = Stock.objects.get(producto=self.producto, almacen=self.almacen)
        self.assertEqual(stock.cantidad_en_mano, 5)

    def test_compra_sin_items_lanza_error(self):
        """Crear una compra sin items debe lanzar ValidationError."""
        with self.assertRaises(ValidationError):
            CompraService.crear_compra_service(
                ubicacion_entrega=self.almacen,
                proveedor=self.proveedor,
                estado_compra=self.estado_pendiente,
                items=[],
                usuario_creador=self.usuario,
            )

    def test_total_compra_calculado_correctamente(self):
        """El total de la orden de compra debe reflejar la suma de subtotales."""
        orden = CompraService.crear_compra_service(
            ubicacion_entrega=self.almacen,
            proveedor=self.proveedor,
            estado_compra=self.estado_pendiente,
            items=[
                {'producto': self.producto, 'cantidad': 3, 'precio_unitario': Decimal('20.00')},
            ],
            usuario_creador=self.usuario,
        )
        self.assertEqual(orden.total, Decimal('60.00'))
