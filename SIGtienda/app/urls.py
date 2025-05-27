from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('fiado/', views.fiado, name='fiado'),
    path('inventario/', views.inventario, name='inventario'),
    path('proveedores/', views.proveedores, name='proveedores'),
    # VENTAS
    path('ventas/', views.ventas, name='ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'), 
    path('ventas/editar/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:venta_id>/', views.eliminar_venta, name='eliminar_venta'), 
    path('api/productos/<int:pk>/precio/', views.obtener_precio_producto, name='obtener_precio_producto'),
]
