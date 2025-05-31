# serializers.py
from rest_framework import serializers
from .models import *


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


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
    class Meta:
        model = Inventario
        fields = '__all__'


class FiadoSerializer(serializers.ModelSerializer):
    cuentaCliente = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Fiado
        fields = '__all__'