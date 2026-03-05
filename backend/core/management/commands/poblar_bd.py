from django.core.management.base import BaseCommand
from categorias.models import Categoria
from productos.models import Marca
from almacenes.models import Almacen
from pagos.models import MedioPago

class Command(BaseCommand):
    help = 'Puebla la BBDD con datos iniciales básicos (catálogos, almacenes, medios de pago)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando carga de datos iniciales...'))

        # 1. Medios de Pago Base
        medios_pago = [
            {'nombre': 'Efectivo', 'descripcion': 'Pago en dinero físico'},
            {'nombre': 'Transferencia Bancaria', 'descripcion': 'Pagos a cuentas bancarias de la empresa'},
            {'nombre': 'Tarjeta de Crédito / Débito', 'descripcion': 'Pagos vía datáfono o link de pago'},
            {'nombre': 'Nequi / Daviplata', 'descripcion': 'Billeteras digitales móviles'}
        ]
        count_pagos = 0
        for mp in medios_pago:
            obj, created = MedioPago.objects.get_or_create(nombre=mp['nombre'], defaults={'descripcion': mp['descripcion']})
            if created:
                count_pagos += 1
        self.stdout.write(self.style.SUCCESS(f'[{count_pagos}] Medios de pago insertados.'))

        # 2. Almacén base para que los productos no fallen al iniciar
        almacen, created = Almacen.objects.get_or_create(
            nombre='Almacén Principal',
            defaults={
                'direccion': 'Dirección por defecto',
                'capacidad': 1000
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('[1] Almacén inicial (Almacén Principal) insertado.'))

        # 3. Categorías por defecto
        categorias = ['Accesorios', 'Mecánica', 'Líquidos']
        count_cat = 0
        for cat_name in categorias:
            obj, created = Categoria.objects.get_or_create(
                nombre=cat_name, 
                defaults={'descripcion': f'Categoría {cat_name}'}
            )
            if created:
                count_cat += 1
        self.stdout.write(self.style.SUCCESS(f'[{count_cat}] Categorías insertadas.'))
        
        # 4. Marcas por defecto
        marcas = ['Genérico', 'Farroad', 'Rodashine', 'Zextour', 'Wanda']
        count_marcas = 0
        for m in marcas:
            obj, created = Marca.objects.get_or_create(
                nombre=m,
                defaults={'descripcion': f'Marca {m}'}
            )
            if created:
                count_marcas += 1
        self.stdout.write(self.style.SUCCESS(f'[{count_marcas}] Marcas insertadas.'))

        self.stdout.write(self.style.SUCCESS('¡La carga de datos iniciales ha finalizado con éxito!'))
