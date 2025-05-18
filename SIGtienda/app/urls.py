from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('ventas/', views.ventas, name='ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'), 
    path('fiado/', views.fiado, name='fiado'),
    path('inventario/', views.inventario, name='inventario'),
    path('proveedores/', views.proveedores, name='proveedores'), 
]
