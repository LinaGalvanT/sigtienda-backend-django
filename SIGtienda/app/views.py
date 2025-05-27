from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, SignupForm, DetalleVentaForm, VentaForm
from .models import Venta, DetalleVenta, Producto


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cedula = form.cleaned_data.get('username')  # 'username' se mapeó a cedula en el formulario
            password = form.cleaned_data.get('password')
            user = authenticate(request, cedula=cedula, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio') 
            else:
                messages.error(request, 'Cédula o contraseña incorrecta.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('inicio') 
    else:
        form = SignupForm()
    return render(request, 'registrar.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def inicio(request):
    
    return render(request, 'inicio.html')

# VENTAS
# ================================================================================
@login_required
def ventas(request):
    query = request.GET.get('q', '')
    ventas_list = Venta.objects.select_related('cliente', 'usuario').all()
    
    if query:
        ventas_list = ventas_list.filter(
            Q(cliente__nombre__icontains=query) |
            Q(cliente__apellido__icontains=query) |
            Q(fechaVenta__icontains=query) |
            Q(id__icontains=query)
        )
    
    return render(request, 'ventas/ventas.html', {
        'ventas': ventas_list,
        'query': query
    })

@login_required
def crear_venta(request):
    DetalleVentaFormSet = formset_factory(DetalleVentaForm, extra=1)
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_formset = DetalleVentaFormSet(request.POST)
        if venta_form.is_valid() and detalle_formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.usuario = request.user
            venta.totalCompra = 0  # Valor temporal para evitar el error por null
            total_venta = 0
            venta.save()
            for form in detalle_formset:
                if form.cleaned_data:
                    detalle = form.save(commit=False)
                    detalle.venta = venta
                    # Asigna el precio del producto seleccionado
                    detalle.precio = detalle.producto.precio
                    detalle.total = detalle.cantidad * detalle.precio
                    total_venta += detalle.total
                    detalle.save()
                    # Actualiza inventario
                    producto = detalle.producto
                    producto.cantidad -= detalle.cantidad
                    producto.save()
            venta.totalCompra = total_venta
            venta.save()
            return redirect('ventas')
    else:
        venta_form = VentaForm()
        detalle_formset = DetalleVentaFormSet()
    return render(request, 'ventas/crear_venta.html', {
        'venta_form': venta_form,
        'detalle_formset': detalle_formset,
    })

def obtener_precio_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return JsonResponse({'precio': producto.precio})

@login_required
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    DetalleVentaFormSet = formset_factory(DetalleVentaForm, extra=0)
    
    if request.method == 'POST':
        venta_form = VentaForm(request.POST, instance=venta)
        detalle_formset = DetalleVentaFormSet(request.POST)
        
        if venta_form.is_valid() and detalle_formset.is_valid():
            # Restaurar inventario antes de actualizar
            for detalle in venta.detalleventa_set.all():
                producto = detalle.producto
                producto.cantidad += detalle.cantidad
                producto.save()
            
            # Actualizar venta
            venta = venta_form.save()
            
            # Actualizar detalles y inventario
            for form in detalle_formset:
                if form.cleaned_data:
                    detalle = form.save(commit=False)
                    detalle.venta = venta
                    detalle.total = detalle.cantidad * detalle.precio
                    detalle.save()
                    
                    # Actualizar inventario
                    producto = detalle.producto
                    producto.cantidad -= detalle.cantidad
                    producto.save()
            
            return redirect('ventas')
    else:
        venta_form = VentaForm(instance=venta)
        detalles = venta.detalleventa_set.all()
        initial_data = [{
            'producto': detalle.producto,
            'cantidad': detalle.cantidad,
            'precio': detalle.precio
        } for detalle in detalles]
        detalle_formset = DetalleVentaFormSet(initial=initial_data)
    
    return render(request, 'ventas/crear_venta.html', {
        'venta_form': venta_form,
        'detalle_formset': detalle_formset,
        'edicion': True
    })

@login_required
def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        # Restaurar inventario
        for detalle in venta.detalleventa_set.all():
            producto = detalle.producto
            producto.cantidad += detalle.cantidad
            producto.save()
        venta.delete()
        messages.success(request, 'Venta eliminada correctamente.')
        return redirect('ventas')
    return render(request, 'ventas/confirmar_eliminar.html', {'venta': venta})

# FIADO
#================================================================

@login_required
def fiado(request):
    return render(request, 'fiado.html')

def inventario(request):
    return render(request, 'inventario.html')

@login_required
def proveedores(request):
    return render(request, 'proveedores.html')