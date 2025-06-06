# views.py
from datetime import date
from django.db.models import Max
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Venta, DetalleVenta, Producto, Cliente
from .serializers import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notificaciones(request):
    # Stock bajo
    inventarios = Inventario.objects.select_related('producto').all()
    bajos = []
    for inv in inventarios:
        if inv.stock <= inv.stockMinimo:
            bajos.append({
                "tipo": "stock_bajo",
                "producto": inv.producto.nombreProducto,
                "stock": inv.stock,
                "stockMinimo": inv.stockMinimo,
                "id": inv.id
            })

    # Lotes próximos a vencer
    hoy = date.today()
    lotes = Lote.objects.select_related('producto__categoria').all()
    por_vencer = []
    for lote in lotes:
        if lote.fecha_vencimiento:
            dias_alerta = getattr(lote.producto.categoria, 'dias_alerta_vencimiento', 15)
            dias_para_vencer = (lote.fecha_vencimiento - hoy).days
            if 0 <= dias_para_vencer <= dias_alerta:
                por_vencer.append({
                    "tipo": "por_vencer",
                    "producto": lote.producto.nombreProducto,
                    "numero_lote": lote.numero_lote,
                    "fecha_vencimiento": lote.fecha_vencimiento,
                    "dias_para_vencer": dias_para_vencer,
                    "cantidad": lote.cantidad,
                    "id": lote.id
                })

    return Response({
        "stock_bajo": bajos,
        "por_vencer": por_vencer,
        "total": len(bajos) + len(por_vencer)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "nombre": user.nombre,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "acceso_ventas": user.acceso_ventas,
        "acceso_inventario": user.acceso_inventario,
        "acceso_productos": user.acceso_productos,
        "acceso_proveedores": user.acceso_proveedores,
        "acceso_compras": user.acceso_compras,
        "acceso_clientes": user.acceso_clientes,
        "acceso_cuentas": user.acceso_cuentas,
    })

class ClienteHistorialView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cliente_id):
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cuenta = CuentaCliente.objects.get(cliente=cliente)
            serializer = CuentaClienteSerializer(cuenta)
            return Response(serializer.data)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=404)

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def descontar_stock_fifo(self, producto, cantidad_vendida):
        lotes = Lote.objects.filter(producto=producto, cantidad__gt=0).order_by('fecha_vencimiento', 'fecha_ingreso')
        cantidad_restante = cantidad_vendida
        for lote in lotes:
            if lote.cantidad >= cantidad_restante:
                lote.cantidad -= cantidad_restante
                lote.save()
                break
            else:
                cantidad_restante -= lote.cantidad
                lote.cantidad = 0
                lote.save()
        if cantidad_restante > 0:
            print("No hay suficiente stock en los lotes para completar la venta.")

    def create(self, request, *args, **kwargs):
        producto_id = request.data.get('producto')
        cantidad = int(request.data.get('cantidad', 0))
        try:
            inventario = Inventario.objects.get(producto=producto_id)
            if inventario.stock < cantidad:
                return Response(
                    {"error": "No hay suficiente stock para este producto."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Inventario.DoesNotExist:
            return Response(
                {"error": "No existe inventario para este producto."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Descontar stock FIFO en lotes
        self.descontar_stock_fifo(producto_id, cantidad)
        return super().create(request, *args, **kwargs)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class FiadoViewSet(viewsets.ModelViewSet):
    queryset = Fiado.objects.all()
    serializer_class = FiadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        venta = serializer.validated_data['venta']
        cliente = venta.cliente
        cuenta, creada = CuentaCliente.objects.get_or_create(cliente=cliente)
        serializer.save(cuentaCliente=cuenta)


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        detalle = serializer.save()
        # Solo si el pedido está recibido/entregado
        if detalle.pedido.estado == 'entregado':
            inventario, creada = Inventario.objects.get_or_create(
                producto=detalle.producto,
                defaults={'stock': 0}
            )
            inventario.stock += detalle.cantidad
            inventario.save()

            # Asignar número de lote automáticamente
            ultimo_lote = Lote.objects.filter(producto=detalle.producto).aggregate(Max('id'))['id__max'] or 0
            numero_lote = f"{detalle.producto}-{ultimo_lote + 1}"

            Lote.objects.create(
                producto=detalle.producto,
                cantidad=detalle.cantidad,
                fecha_vencimiento=detalle.fecha_vencimiento,  # o como llegue del frontend
                numero_lote=numero_lote
            )


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marcas.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.IsAuthenticated]


class UnidadDeMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadDeMedida.objects.all()
    serializer_class = UnidadDeMedidaSerializer
    permission_classes = [permissions.IsAuthenticated]


class TipoEmpaqueViewSet(viewsets.ModelViewSet):
    queryset = TipoEmpaque.objects.all()
    serializer_class = TipoEmpaqueSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [permissions.IsAuthenticated]
