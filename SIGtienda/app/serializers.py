# serializers.py
from rest_framework import serializers
from .models import *

class ProductoSerializer(serializers.ModelSerializer):

    stock = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = '__all__'

    def get_stock(self, obj):
        # Busca el inventario relacionado
        inventario = Inventario.objects.filter(producto=obj).first()
        return inventario.stock if inventario else 0


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    detalleventa_set = DetalleVentaSerializer(many=True, read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    cliente_nombre = serializers.CharField(
        source="cliente.nombre", read_only=True)
    es_fiado = serializers.SerializerMethodField()

    def get_es_fiado(self, obj):
        # Retorna True si hay un fiado asociado a esta venta
        return Fiado.objects.filter(venta=obj).exists()

    class Meta:
        model = Venta
        fields = '__all__'


class InventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombreProducto", read_only=True)
    estado_legible = serializers.CharField(source="get_estadoProducto_display", read_only=True)
    
    class Meta:
        model = Inventario
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    fecha_vencimiento = serializers.DateField(read_only=True, required=False)

    class Meta:
        model = DetallePedido
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marcas
        fields = '__all__'

class UnidadDeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadDeMedida
        fields = '__all__'

class TipoEmpaqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEmpaque
        fields = '__all__'

class LoteSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombreProducto", read_only=True)
    class Meta:
        model = Lote
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'fecha', 'cantidad', 'esAbono']

class FiadoSerializer(serializers.ModelSerializer):
    pagos = PagoSerializer(many=True, read_only=True)  # Pagos asociados al fiado
    venta = VentaSerializer(read_only=True)  # Detalles de la venta fiada

    class Meta:
        model = Fiado
        fields = ['id', 'venta', 'montoDeuda', 'fechaUltimoPago', 'pagos']

class CuentaClienteSerializer(serializers.ModelSerializer):
    fiados = FiadoSerializer(many=True, read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)

    class Meta:
        model = CuentaCliente
        fields = ['id', 'montoTotal', 'fiados', 'pagos']

class ClienteSerializer(serializers.ModelSerializer):
    cuenta = CuentaClienteSerializer(read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'telefono', 'cuenta']