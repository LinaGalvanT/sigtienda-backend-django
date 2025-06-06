# admin.py
from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Marcas)
admin.site.register(UnidadDeMedida)
admin.site.register(TipoEmpaque)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Inventario)
admin.site.register(Fiado)
admin.site.register(Lote)
admin.site.register(CuentaCliente)