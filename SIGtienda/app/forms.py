from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Venta, DetalleVenta


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Cédula', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234567898'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '*********'
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('cedula', 'nombre', 'apellido', 'email', 'password1', 'password2')

    cedula = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '12345678'
    }))
    nombre = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre del Usuario'
    }))
    apellido = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apellido del Usuario'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'prueba@prueba.com'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '********'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '********'
    }))
    
    # Formulario para la venta principal
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'fechaVenta', 'totalCompra']
        widgets = {
            'fechaVenta': forms.DateInput(attrs={'type': 'date'}),
        }

# Formulario para los detalles de la venta (productos)
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }