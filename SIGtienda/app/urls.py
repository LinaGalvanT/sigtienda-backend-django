# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

router = DefaultRouter()
router.register(r'ventas', VentaViewSet)
router.register(r'detalleventas', DetalleVentaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'fiados', FiadoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detallepedidos', DetallePedidoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'unidadesdemedida', UnidadDeMedidaViewSet)
router.register(r'tipoempaques', TipoEmpaqueViewSet)
router.register(r'lotes', LoteViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/current_user/', current_user),
    path('api/notificaciones/', notificaciones),
    path('api/clientes/<int:cliente_id>/historial/', ClienteHistorialView.as_view()),
]
