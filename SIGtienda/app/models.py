# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Categoria(models.Model):
    nombreCategoria = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    codigoCategoria = models.CharField(max_length=50)
    dias_alerta_vencimiento = models.IntegerField(default=15) 

    def __str__(self):
        return self.nombreCategoria

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class CuentaCliente(models.Model):
    montoTotal = models.FloatField(default=0.0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Cuenta de cliente"
        verbose_name_plural = "Cuentas de clientes"


class Marcas(models.Model):
    nombreMarca = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreMarca

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"


class Proveedor(models.Model):
    nombreProveedor = models.CharField(max_length=50)
    nombreContacto = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    email = models.EmailField()
    comentarios = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    fechaPedido = models.DateField()
    total = models.FloatField()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class Pago(models.Model):
    cantidad = models.IntegerField()
    fecha = models.DateField()
    esAbono = models.BooleanField()
    cuentaCliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

class TipoEmpaque(models.Model):
    nombreTipoEmpaque = models.CharField(max_length=50)
    models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + " - " + self.nombreTipoEmpaque

    class Meta:
        verbose_name = "Tipo de empaque"
        verbose_name_plural = "Tipos de empaque"


class UnidadDeMedida(models.Model):
    nombreUnidadDeMedida = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreUnidadDeMedida

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"


class CustomUserManager(BaseUserManager):
    def create_user(self, cedula, email, password=None, **extra_fields):
        if not cedula:
            raise ValueError('El campo cédula es obligatorio')
        if not email:
            raise ValueError('El campo email es obligatorio')

        email = self.normalize_email(email)
        user = self.model(cedula=cedula, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(cedula, email, password, **extra_fields)


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido')
    cedula = models.CharField(
        max_length=50, unique=True, null=True, blank=True, verbose_name='Cédula')
    email = models.EmailField(unique=True, blank=False,
                              verbose_name='Correo electrónico')
    acceso_ventas = models.BooleanField(default=True)
    acceso_inventario = models.BooleanField(default=True)
    acceso_productos = models.BooleanField(default=True)
    acceso_proveedores = models.BooleanField(default=True)
    acceso_compras = models.BooleanField(default=True)
    acceso_clientes = models.BooleanField(default=True)
    acceso_cuentas = models.BooleanField(default=True)
    # Sobreescribimos el campo username                              
    username = None
    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaVenta = models.DateField()
    totalCompra = models.FloatField()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"


class Producto(models.Model):
    nombreProducto = models.CharField(max_length=50)
    precio = models.FloatField()
    vidaUtil = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marcas = models.ForeignKey(Marcas, on_delete=models.CASCADE)
    unidadDeMedida = models.ForeignKey(
        UnidadDeMedida, on_delete=models.CASCADE)
    tipoEmpaque = models.ForeignKey(TipoEmpaque, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreProducto

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Inventario(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ]
    estadoProducto = models.CharField(max_length=50, choices=ESTADOS, default='activo')
    stock = models.IntegerField()
    stockMinimo = models.IntegerField(default=0)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.producto.nombreProducto

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    valorpedido = models.FloatField()
    fecha_vencimiento = models.DateField(null=True, blank=True) 

    def __str__(self):
        return str(self.id) + " - " + str(self.producto.nombreProducto)

    class Meta:
        verbose_name = "Detalle de pedido"
        verbose_name_plural = "Detalles de pedido"


class Fiado(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    montoDeuda = models.FloatField()
    fechaUltimoPago = models.DateField()
    cuentaCliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Fiado"
        verbose_name_plural = "Fiados"

class Lote(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='lotes')
    cantidad = models.IntegerField()
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    numero_lote = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Lote {self.numero_lote} - {self.producto.nombreProducto}"