# views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Venta, DetalleVenta, Producto, Cliente
from .serializers import *


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
        # Obtener la venta desde los datos del serializer
        venta = serializer.validated_data['venta']
        cliente = venta.cliente

        # Obtener o crear la cuenta del cliente
        cuenta, creada = CuentaCliente.objects.get_or_create(
            cliente=cliente)

        # Guardar el fiado con la cuenta asociada
        serializer.save(cuentaCliente=cuenta)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "nombre": user.nombre,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        # Otros campos que quieras exponer
    })
